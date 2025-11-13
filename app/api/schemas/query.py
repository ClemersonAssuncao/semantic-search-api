from pydantic import BaseModel
from typing import List
from app.api.schemas.document import DocumentQueryResult

class QueryRequest(BaseModel):
    query: str
    top_k: int | None = None

class QueryResponse(BaseModel):
    query: str
    results: List[DocumentQueryResult]