import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.service_document import ServiceDocument
from sentence_transformers import util
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

sd = ServiceDocument()

docs = sd.get_docs('txt')
doc_embeddings = sd.get_embeddings()

class QueryRequest(BaseModel):
    query: str

app = FastAPI()


@app.post("/query")
async def query_rag(request: QueryRequest):
    """Busca o documento mais relevante usando embeddings e remove sobreposição."""
    query_embedding = sd.model_embedding.encode(request.query, convert_to_tensor=True)

    best_doc = None
    best_score = float("-inf")

    # Calcular similaridade entre a query e cada documento
    for doc in docs:
        scores = util.cos_sim(query_embedding, doc_embeddings[doc["id"]])
        avg_score = scores.mean().item()

        logging.info(f"Doc {doc['id']} - Similaridade: {avg_score}")

        if avg_score > best_score:
            best_score = avg_score
            best_doc = doc

    if best_doc:
        text_continuo = sd.reconstruir_texto(best_doc["chunks"])

        return {
            "best_match": best_doc["id"],
            "avg_score": best_score,
            "texto_completo": text_continuo,
            "fonte": best_doc["filename"]
        }
    else:
        raise HTTPException(status_code=404, detail="Nenhum documento relevante encontrado.")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
