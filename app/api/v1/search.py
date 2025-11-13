from time import time
from fastapi import APIRouter, Depends

from app.api.deps import get_search_service
from app.api.schemas.search import SearchRequest, SearchResponse
from app.core.services.search_service import SearchService

router = APIRouter(prefix="/api/v1/search", tags=["search"])

# TO DO: Analisar performance e logging adequado
@router.get("/")
def search_documents(
    payload: SearchRequest,
    search_service: SearchService = Depends(get_search_service),
):
    start_time = time()
    print("Received search request:", payload)
    results = search_service.search(payload.query, payload.top_k)
    end_time = time()
    print(f"Search took {end_time - start_time:.4f} seconds")
    return SearchResponse(
        query=payload.query,
        results=results
    )

