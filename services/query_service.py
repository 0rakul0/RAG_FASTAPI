import logging
from fastapi import HTTPException
from services.service_document import ServiceDocument
from sentence_transformers import util
from ollama import Client
from utils.guardian_sail import guardian_sail

# Configuração do cliente Ollama
client = Client(
    host='http://localhost:11434',
    headers={'x-some-header': 'some-value'}
)

class QueryService(ServiceDocument):
    def __init__(self):
        super().__init__()
        self.sd = ServiceDocument()
    def query_rag_service(self, query: str):
        # Carregamento de documentos e embeddings
        docs = self.sd.get_docs('txt')
        doc_embeddings = self.sd.get_embeddings()

        """Busca o documento mais relevante usando embeddings e gera resposta."""
        query_embedding = self.sd.model_embedding.encode(query, convert_to_tensor=True)

        best_doc = None
        best_score = float("-inf")

        for doc in docs:
            scores = util.cos_sim(query_embedding, doc_embeddings[doc["id"]])
            avg_score = scores.mean().item()

            logging.info(f"Doc {doc['id']} - Similaridade: {avg_score}")

            if avg_score > best_score:
                best_score = avg_score
                best_doc = doc

        if best_doc:
            texto_completo = self.sd.reconstruir_texto(best_doc["chunks"])

            prompt = f"Você é uma assistente de IA, que responde baseado somente no documento:\n {texto_completo}\n\n User:{query}\n resposta"

            try:
                response = client.chat(model="llama3.1", messages=[
                    {"role": "system", "content": prompt}
                ])
                resposta_filtrada = guardian_sail(response['message']['content'])
                return {
                    "pergunta": query,
                    "response": resposta_filtrada,
                    "documento_fonte": best_doc["filename"]
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        else:
            raise HTTPException(status_code=404, detail="Nenhum documento relevante encontrado.")
