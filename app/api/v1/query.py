from time import time
from fastapi import APIRouter, Depends

from app.api.deps import get_query_service
from app.api.schemas.query import QueryRequest, QueryResponse
from app.core.services.query_service import QueryService

router = APIRouter(prefix="/api/v1/query", tags=["query"])

# TO DO: Analisar performance e logging adequado
@router.get("/")
def query_documents(
    payload: QueryRequest,
    query_service: QueryService = Depends(get_query_service),
):
    '''Perform a semantic search query and return the top matching documents.'''
    results = query_service.search(payload.query, payload.top_k)
    return QueryResponse(
        query=payload.query,
        results=results
    )

