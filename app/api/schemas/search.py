from pydantic import BaseModel
from typing import List
from app.api.schemas.document import DocumentSearchResult

class SearchRequest(BaseModel):
    query: str
    top_k: int | None = None

class SearchResponse(BaseModel):
    query: str
    results: List[DocumentSearchResult]