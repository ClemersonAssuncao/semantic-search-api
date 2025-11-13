from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from repositories.document_repository import DocumentRepository

def get_document_repository(db: Session = Depends(get_db)):
    return DocumentRepository(db)
