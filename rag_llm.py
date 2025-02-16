import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from service_document import get_docs, get_embeddings, model_embedding
from sentence_transformers import util
import logging
from ollama import Client

client = Client(
    host='http://localhost:11434',
    headers={'x-some-header': 'some-value'}
)

# Configurar logging
logging.basicConfig(level=logging.INFO)


docs = get_docs()
doc_embeddings = get_embeddings()

class QueryRequest(BaseModel):
    query: str


app = FastAPI()


@app.post("/query")
async def query_rag(request: QueryRequest):
    """Busca o documento mais relevante usando embeddings."""
    query_embedding = model_embedding.encode(request.query, convert_to_tensor=True)

    best_doc = None
    best_score = float("-inf")

    # Calcular similaridade entre a query e cada documento
    for doc in docs:
        scores = util.cos_sim(query_embedding, doc_embeddings[doc["id"]])
        avg_score = scores.mean().item()  # Média das similaridades dos chunks

        logging.info(f"Doc {doc['id']} - Similaridade: {avg_score}")

        if avg_score > best_score:
            best_score = avg_score
            best_doc = doc

    promopt = f"Você é uma assistente de IA, que responde baseado somente no documento:\n {best_doc['chunks']}\n\n User:{request.query}\n resposta"

    try:
        response = client.chat(model="llama3.1", messages=[
            {"role": "system", "content": promopt}
        ])
        return {"pergunta": request.query,"response":response['message']['content'], "documento_fonte": best_doc["filename"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
