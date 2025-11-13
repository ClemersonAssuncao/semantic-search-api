from typing import List
from sqlalchemy.orm import Session
from app.infrastructure.persistence.models.document import DocumentModel


class DocumentRepository:
    '''Repository to manage DocumentModel persistence.'''
    def __init__(self, db: Session):
        self.db = db

    # Acabei não usando esse método por enquanto
    def create(self, doc: DocumentModel) -> DocumentModel:
        '''Create a single DocumentModel instance in the database.'''
        self.db.add(doc)
        self.db.commit()
        self.db.refresh(doc)
        return doc

    def create_many(self, docs: List[DocumentModel]) -> List[DocumentModel]:
        '''Create multiple DocumentModel instances in the database.'''
        self.db.add_all(docs)
        self.db.commit()
        for d in docs:
            self.db.refresh(d)
        return docs

    def list_all(self) -> List[DocumentModel]:
        '''List all DocumentModel instances from the database.'''
        return self.db.query(DocumentModel).all()
    
    def get_by_id(self, document_id: int) -> DocumentModel | None:
        '''Get a DocumentModel instance by its ID.'''
        return self.db.query(DocumentModel).filter(DocumentModel.id == document_id).first()