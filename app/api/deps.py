from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.services.search_service import SearchService

from app.infrastructure.persistence.db.session import get_db
from app.infrastructure.persistence.repositories.document_repository import DocumentRepository

from app.core.services.embedding_service import EmbeddingService

def get_document_repository(db: Session = Depends(get_db)) -> DocumentRepository:
    return DocumentRepository(db)

def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()

def get_search_service(
    repo: DocumentRepository = Depends(get_document_repository),
    emb: EmbeddingService = Depends(get_embedding_service),
) -> SearchService:
    return SearchService(repo, emb)