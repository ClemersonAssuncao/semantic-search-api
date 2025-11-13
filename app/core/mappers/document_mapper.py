from app.infrastructure.persistence.models.document import DocumentModel
from app.api.schemas.document import DocumentCreate, DocumentRead

class DocumentMapper:
    '''Mapper to convert between Document DTOs and ORM models.'''

    @staticmethod
    def to_model(dto: DocumentCreate, embeddings) -> DocumentModel:
        '''Converts a DocumentCreate DTO to a DocumentModel for persistence.'''
        return DocumentModel(
            title=dto.title,
            content=dto.content,
            embedding=embeddings.tobytes() if hasattr(embeddings, 'tobytes') else embeddings,
        )
    
    @staticmethod
    def to_read(model: DocumentModel) -> DocumentRead:
        '''Converts a DocumentModel to a DocumentRead DTO for API responses.'''
        return DocumentRead(
            id=model.id,
            title=model.title,
            content=model.content
        )
    
