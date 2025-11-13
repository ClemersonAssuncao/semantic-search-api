from fastapi import APIRouter, Depends

from app.api.deps import get_search_service
from app.api.schemas.search import SearchRequest, SearchResponse
from app.core.services.search_service import SearchService

router = APIRouter(prefix="/api/v1/search", tags=["search"])

@router.get("/")
def search_documents(
    payload: SearchRequest,
    search_service: SearchService = Depends(get_search_service),
):
    results = search_service.search(payload.query, payload.top_k)
    # Aqui vou montar um service para isso
    return SearchResponse(
        query=payload.query,
        results=results
    )

