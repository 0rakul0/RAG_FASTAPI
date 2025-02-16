import os

def load_txt_files(directory, chunk_size=512, overlap=128):
    """Lê arquivos .txt de um diretório e retorna uma lista de documentos processados com chunks."""
    docs = []
    doc_id = 1  # ID único para cada documento

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            chunks = create_chunks(content, chunk_size, overlap)

            if chunks:
                docs.append({
                    'id': doc_id,
                    'filename': filename,
                    'chunks': chunks,
                    'metadata': {'file_name': filename}
                })
                doc_id += 1

    return docs
def create_chunks(text, chunk_size=512, overlap=128):
    """Divide o texto em chunks sem sobreposição redundante."""
    paragraphs = text.split(". \n\n")  # Quebra em frases completas
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) + 2 > chunk_size:
            chunks.append(current_chunk.strip())
            # Mantém um overlap apenas se houver espaço suficiente
            words = current_chunk.split()
            current_chunk = " ".join(words[-(overlap // 5):]) if len(words) > overlap // 5 else ""
        current_chunk += paragraph + ". \n\n"

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks
