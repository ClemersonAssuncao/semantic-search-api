from pydantic import BaseModel

class DocumentBase(BaseModel):
    title: str
    content: str

class DocumentCreate(DocumentBase):
    pass

class DocumentRead(DocumentBase):
    id: int

class DocumentQueryResult(BaseModel):
    id: int
    title: str
    score: float


