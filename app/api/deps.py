from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.persistence.db.session import get_db
from app.infrastructure.persistence.repositories.document_repository import DocumentRepository

def get_document_repository(db: Session = Depends(get_db)):
    return DocumentRepository(db)
