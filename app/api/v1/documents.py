from typing import List
from fastapi import APIRouter, Depends
from requests import Session

from app.db.session import get_db
from app.schemas.document import DocumentRead, DocumentCreate
from mappers.document_mapper import DocumentMapper
from repositories.document_repository import DocumentRepository

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])

@router.post("/", response_model=List[DocumentRead])
def create_document(
    payload: List[DocumentCreate],
    db: Session = Depends(get_db),
):
    
    repo = DocumentRepository(db)

    # Aqui vou gerar os embeddings mais tarde
    contents = [doc.content for doc in payload]

    models = [
        DocumentMapper.to_model(doc) for doc in payload
    ]
    
    saved_docs = repo.create_many(models)
    return [DocumentMapper.to_read(doc) for doc in saved_docs]