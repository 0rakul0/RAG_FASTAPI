import os
import fitz  # PyMuPDF
from service_txt import create_chunks

def extract_text_from_pdf(pdf_path):
    """Extrai texto de um arquivo PDF e retorna uma lista de dicionários com número da página e texto."""
    doc = fitz.open(pdf_path)
    pdf_content = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        if text.strip():  # Verifica se a página não está vazia
            pdf_content.append({'page_number': page_num + 1, 'text': text})

    return pdf_content

def load_pdf_files(directory, chunk_size=512, overlap=128):
    """Lê arquivos .pdf de um diretório e retorna uma lista de documentos processados com chunks e metadados."""
    docs = []
    doc_id = 1  # ID único para cada documento

    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            pdf_content = extract_text_from_pdf(file_path)

            for page in pdf_content:
                chunks = create_chunks(page['text'], chunk_size, overlap)
                for idx, chunk in enumerate(chunks):
                    docs.append({
                        'id': doc_id,
                        'filename': filename,
                        'chunks': [chunk],
                        'metadata': {
                            'file_name': filename,
                            'page_number': page['page_number'],
                            'chunk_index': idx + 1
                        }
                    })
                    doc_id += 1

    return docs
