from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.persistence.db.session import get_db
from app.infrastructure.persistence.repositories.document_repository import DocumentRepository

from app.core.services.embedding_service import EmbeddingService

def get_document_repository(db: Session = Depends(get_db)) -> DocumentRepository:
    return DocumentRepository(db)

def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()