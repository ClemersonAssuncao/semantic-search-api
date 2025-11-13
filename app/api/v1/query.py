import logging
from time import time
from fastapi import APIRouter, Depends, Query

from app.api.deps import get_query_service
from app.api.schemas.query import QueryResponse, QueryRequest
from app.core.services.query_service import QueryService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/query", tags=["query"])


@router.get("/", response_model=QueryResponse)
def query_documents(
    payload: QueryRequest,
    query_service: QueryService = Depends(get_query_service),
):
    '''Perform a semantic search query and return the top matching documents.'''
    logger.info(f"Received query: '{payload.query}' with top_k={payload.top_k}")
    start_time = time()
    
    results = query_service.search(payload.query, payload.top_k)
    
    elapsed_time = time() - start_time
    logger.info(f"Query completed in {elapsed_time:.3f}s, found {len(results)} results")
    logger.debug(f"Top result scores: {[r.score for r in results[:3]]}")
    
    return QueryResponse(
        query=payload.query,
        results=results
    )

