from pydantic import BaseModel
from typing import List
from app.api.schemas.document import DocumentSearchResult

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    results: List[DocumentSearchResult]