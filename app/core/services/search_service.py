from functools import lru_cache
from typing import List
import numpy as np

from app.infrastructure.settings import settings
from app.infrastructure.persistence.repositories.document_repository import DocumentRepository
from app.core.services.embedding_service import EmbeddingService
from app.api.schemas.search import SearchResponse, DocumentSearchResult

class SearchService:

    def __init__(self, 
                 repo: DocumentRepository, 
                 embedding_service: EmbeddingService):
        self.repo = repo
        self.embedding_service = embedding_service
        pass

    def search(self, query: str, top_k: int | None = None) -> List[DocumentSearchResult]:
        top_k = top_k or settings.default_search_top_k
        query_embedding = self.embedding_service.embed_texts([query])[0]

        documents = self.repo.list_all()

        if not documents:
            return []

        doc_embeddings = np.vstack([
            np.frombuffer(doc.embedding, dtype=np.float32) for doc in documents
        ])

        query_embedding = self.embedding_service.embed_texts([query])[0]

        # similaridade coseno
        doc_norms = np.linalg.norm(doc_embeddings, axis=1)
        query_norm = np.linalg.norm(query_embedding)
        sims = (doc_embeddings @ query_embedding) / (doc_norms * query_norm + 1e-10)

        indices = np.argsort(-sims)[:top_k]

        results: List[DocumentSearchResult] = []
        for idx in indices:
            doc = documents[idx]
            results.append(
                DocumentSearchResult(
                    id=doc.id,
                    title=doc.title,
                    score=float(sims[idx]),
                )
            )
        return results