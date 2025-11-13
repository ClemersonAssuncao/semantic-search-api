from functools import lru_cache
from typing import List
import numpy as np

from app.infrastructure.settings import settings
from app.infrastructure.persistence.repositories.document_repository import DocumentRepository
from app.core.services.embedding_service import EmbeddingService
from app.api.schemas.query import DocumentQueryResult

class QueryService:
    '''Service to perform semantic search queries.'''

    def __init__(self, 
                 repo: DocumentRepository, 
                 embedding_service: EmbeddingService):
        self.repo = repo
        self.embedding_service = embedding_service
        pass

    def search(self, query: str, top_k: int | None = None) -> List[DocumentQueryResult]:
        top_k = top_k or settings.default_query_top_k

        documents = self.repo.list_all()

        if not documents:
            return []

        doc_embeddings = np.vstack([
            np.frombuffer(doc.embedding, dtype=np.float32) for doc in documents
        ])

        # similaridade coseno
        query_embedding = self.embedding_service.embed_texts([query])[0]
        sims = self._cosine_similarities(doc_embeddings, query_embedding)

        top_k = min(top_k, len(documents))
        indices = np.argsort(-sims)[:top_k]

        results: List[DocumentQueryResult] = []
        for idx in indices:
            doc = documents[idx]
            results.append(
                DocumentQueryResult(
                    id=doc.id,
                    title=doc.title,
                    score=float(sims[idx]),
                )
            )
        return results
    
    def _cosine_similarities(self, doc_embeddings: np.ndarray, query_embedding: np.ndarray) -> np.ndarray:
        return (doc_embeddings @ query_embedding)