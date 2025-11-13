from sqlalchemy import Column, Integer, String, LargeBinary
from app.infrastructure.persistence.db.base import Base

class DocumentModel(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=False)
    embedding = Column(LargeBinary, nullable=False)