from typing import List
from fastapi import status, APIRouter, Depends, HTTPException
from requests import Session

from app.api.schemas.document import DocumentRead, DocumentCreate

from app.core.services.embedding_service import EmbeddingService, get_embedding_service
from app.core.mappers.document_mapper import DocumentMapper

from app.infrastructure.persistence.db.session import get_db
from app.infrastructure.persistence.repositories.document_repository import DocumentRepository

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])

# Endpoint to create multiple documents
@router.post(
    "/", 
    response_model=List[DocumentRead],
    status_code=status.HTTP_201_CREATED
)
def create_document(
    payload: List[DocumentCreate],
    db: Session = Depends(get_db),
    embedding_service: EmbeddingService = Depends(get_embedding_service),
):
    
    repo = DocumentRepository(db)

    # Aqui vou gerar os embeddings mais tarde
    contents = [doc.content for doc in payload]
    embeddings = embedding_service.embed_texts(contents)

    models = [
        DocumentMapper.to_model(doc, emb)
        for doc, emb in zip(payload, embeddings)
    ]
    
    saved_docs = repo.create_many(models)
    return [DocumentMapper.to_read(doc) for doc in saved_docs]

# Endpoint to list all documents
@router.get("/", response_model=List[DocumentRead])
def list_documents(
    db: Session = Depends(get_db),
):
    repo = DocumentRepository(db)
    documents = repo.list_all()
    return [DocumentMapper.to_read(doc) for doc in documents]

# Endpoint to get a document by ID
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