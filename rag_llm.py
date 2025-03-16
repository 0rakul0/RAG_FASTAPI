import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from services.query_service import QueryService

class QueryRequest(BaseModel):
    query: str

app = FastAPI()

qrs = QueryService()

@app.post("/query")
async def query_rag(request: QueryRequest):
    """Endpoint para buscar um documento relevante e gerar resposta."""
    result = qrs.query_rag_service(request.query)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
