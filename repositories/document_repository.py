from typing import List
from sqlalchemy.orm import Session
from app.models.document import DocumentModel


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, doc: DocumentModel) -> DocumentModel:
        self.db.add(doc)
        self.db.commit()
        self.db.refresh(doc)
        return doc

    def create_many(self, docs: List[DocumentModel]) -> List[DocumentModel]:
        self.db.add_all(docs)
        self.db.commit()
        for d in docs:
            self.db.refresh(d)
        return docs

    def list_all(self) -> List[DocumentModel]:
        return self.db.query(DocumentModel).all()