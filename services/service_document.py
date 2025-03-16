import os
import logging
from sentence_transformers import SentenceTransformer
from services.service_txt import load_txt_files
from services.service_pdf import load_pdf_files

# Configurar logging
logging.basicConfig(level=logging.INFO)

class ServiceDocument(object):
    def __init__(self):
        self.DATA_DIR = "./data"
        self.model_embedding = SentenceTransformer("all-MiniLM-L6-v2")


    def load_documents(self, directory, file_types=("txt", "pdf")):
        """
        Lê arquivos de um diretório e retorna uma lista de documentos processados.

        :param directory: Diretório contendo os arquivos.
        :param file_types: Tupla indicando os tipos de arquivos a carregar ("txt", "pdf" ou ambos).
        :return: Lista de documentos processados.
        """
        docs = []

        if not os.path.exists(directory):
            logging.warning(f"O diretório {directory} não existe. Criando...")
            os.makedirs(directory, exist_ok=True)

        if "txt" in file_types:
            docs.extend(load_txt_files(directory))

        if "pdf" in file_types:
            docs.extend(load_pdf_files(directory))

        return docs

    def generate_embeddings(self, docs):
        """
        Gera embeddings para cada chunk nos documentos.

        :param docs: Lista de documentos processados.
        :return: Dicionário com embeddings {documento_id: embeddings}
        """
        doc_embeddings = {}

        for doc in docs:
            if "chunks" not in doc:
                logging.warning(f"Documento {doc.get('id', 'desconhecido')} sem chunks. Pulando...")
                continue

            embeddings = self.model_embedding.encode(doc['chunks'], convert_to_tensor=True)
            doc_embeddings[doc['id']] = embeddings

        return doc_embeddings


    def get_docs(self, ext):
        """
        Retorna a lista de documentos com base na extensão.

        :param ext: Tipo de documento ('txt', 'pdf' ou 'all').
        :return: Lista de documentos do tipo especificado.
        """
        if ext == 'txt':
            docs_txt = self.load_documents(self.DATA_DIR, file_types=("txt",))
            return docs_txt
        elif ext == 'pdf':
            docs_pdf = self.load_documents(self.DATA_DIR, file_types=("pdf",))
            return docs_pdf
        elif ext == 'all':
            docs_all = self.load_documents(self.DATA_DIR)
            return docs_all
        else:
            logging.error(f"Extensão inválida: {ext}. Use 'txt', 'pdf' ou 'all'.")
            return []


    def get_embeddings(self):
        """
        Retorna os embeddings calculados dos documentos.

        :return: Dicionário com embeddings {documento_id: embeddings}
        """
        doc_embeddings = self.generate_embeddings(self.get_docs('all'))
        return doc_embeddings

    def reconstruir_texto(self, chunks, overlap=128):
        """Remove o overlap dos chunks e reconstrói um texto contínuo."""
        texto_final = chunks[0]

        for i in range(1, len(chunks)):
            texto_final += chunks[i][overlap:]  # Remove a parte sobreposta

        return texto_final.strip()