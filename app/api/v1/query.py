from fastapi import APIRouter

from app.api.schemas.query import QueryRequest, QueryResponse

router = APIRouter(prefix="/api/v1/query", tags=["query"])

@router.get("/")
def query_documents(
    payload: QueryRequest
):
    # Aqui vou montar um service para isso
    return QueryResponse(
        query=payload.query,
        results=[]
    )

