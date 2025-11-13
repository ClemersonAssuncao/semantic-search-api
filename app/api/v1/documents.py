from typing import List
from fastapi import APIRouter, Depends, HTTPException
from requests import Session

from app.infrastructure.persistence.db.session import get_db
from app.infrastructure.persistence.repositories.document_repository import DocumentRepository
from app.api.schemas.document import DocumentRead, DocumentCreate
from app.core.mappers.document_mapper import DocumentMapper

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

@router.get("/", response_model=List[DocumentRead])
def list_documents(
    db: Session = Depends(get_db),
):
    repo = DocumentRepository(db)
    documents = repo.list_all()
    return [DocumentMapper.to_read(doc) for doc in documents]

@router.get("/{document_id}", response_model=DocumentRead)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    repo = DocumentRepository(db)
    document = repo.get_by_id(document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return DocumentMapper.to_read(document)