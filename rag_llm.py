import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from services.query_service import query_rag_service  # Importando o services

class QueryRequest(BaseModel):
    query: str

app = FastAPI()

@app.post("/query")
async def query_rag(request: QueryRequest):
    """Endpoint para buscar um documento relevante e gerar resposta."""
    return query_rag_service(request.query)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
