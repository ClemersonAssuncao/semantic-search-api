import logging
from functools import lru_cache
from typing import List
import numpy as np

from sentence_transformers import SentenceTransformer
from app.infrastructure.settings import settings

logger = logging.getLogger(__name__)

class EmbeddingService:
    '''Service to generate text embeddings using a pre-trained model.'''
    
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or settings.embedding_model_name
        logger.info(f"Loading embedding model: {self.model_name}")
        self._model = SentenceTransformer(self.model_name)
        logger.info(f"Embedding model loaded successfully")

    @property
    def model(self) -> SentenceTransformer:
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        logger.debug(f"Encoding {len(texts)} texts with model {self.model_name}")
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings = embeddings / (norms + 1e-10)
        logger.debug(f"Generated normalized embeddings with shape {embeddings.shape}")
        return embeddings

@lru_cache
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()