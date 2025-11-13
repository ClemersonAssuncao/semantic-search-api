from app.infrastructure.persistence.models.document import DocumentModel
from app.api.schemas.document import DocumentCreate, DocumentRead

class DocumentMapper:
    @staticmethod
    def to_model(dto: DocumentCreate) -> DocumentModel:
        # Converte DTO >> ORM Model (para persistir).
        return DocumentModel(
            title=dto.title,
            content=dto.content
        )
    
    @staticmethod
    def to_read(model: DocumentModel) -> DocumentRead:
        # Converte ORM Model >> DTO para API.
        return DocumentRead(
            id=model.id,
            title=model.title,
            content=model.content
        )
    
