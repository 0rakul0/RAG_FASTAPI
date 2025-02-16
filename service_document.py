import os

from sentence_transformers import SentenceTransformer
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

DATA_DIR = "data"

# Lista de documentos com chunks como listas de frases
def load_txt_files(directory):
    """Lê arquivos .txt de um diretório e retorna uma lista de documentos com chunks."""
    docs = []
    doc_id = 1  # ID único para cada documento

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            # Dividir o conteúdo em chunks (por parágrafo)
            chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]

            if chunks:
                docs.append({"id": doc_id, "filename": filename, "chunks": chunks})
                doc_id += 1

    return docs

docs = load_txt_files(DATA_DIR)

# Carregar modelo de embeddings
model_embedding = SentenceTransformer("all-MiniLM-L6-v2")

# Criar embeddings para cada chunk (e não o documento inteiro)
doc_embeddings = {
    doc["id"]: model_embedding.encode(doc["chunks"], convert_to_tensor=True)
    for doc in docs
}

def get_docs():
    """Retorna a lista de documentos."""
    return docs

def get_embeddings():
    """Retorna os embeddings calculados dos documentos."""
    return doc_embeddings
