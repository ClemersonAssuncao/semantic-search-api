"""Tests for QueryService."""
import pytest
import numpy as np
from unittest.mock import Mock, MagicMock

from app.core.services.query_service import QueryService
from app.api.schemas.query import DocumentQueryResult
from app.infrastructure.persistence.models.document import DocumentModel


class TestQueryService:
    """Test suite for QueryService class."""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock DocumentRepository."""
        return Mock()

    @pytest.fixture
    def mock_embedding_service(self):
        """Create a mock EmbeddingService."""
        return Mock()

    @pytest.fixture
    def query_service(self, mock_repository, mock_embedding_service):
        """Create a QueryService instance with mocked dependencies."""
        return QueryService(
            repo=mock_repository,
            embedding_service=mock_embedding_service
        )

    @pytest.fixture
    def sample_documents(self):
        """Create sample documents with embeddings."""
        # Create normalized embeddings
        emb1 = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        emb2 = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        emb3 = np.array([0.7071, 0.7071, 0.0], dtype=np.float32)
        
        doc1 = DocumentModel(
            id=1,
            title="Document 1",
            content="Content 1",
            embedding=emb1.tobytes()
        )
        doc2 = DocumentModel(
            id=2,
            title="Document 2",
            content="Content 2",
            embedding=emb2.tobytes()
        )
        doc3 = DocumentModel(
            id=3,
            title="Document 3",
            content="Content 3",
            embedding=emb3.tobytes()
        )
        return [doc1, doc2, doc3]

    def test_search_returns_empty_when_no_documents(
        self, query_service, mock_repository, mock_embedding_service
    ):
        """Test search returns empty list when repository has no documents."""
        mock_repository.list_all.return_value = []
        
        results = query_service.search("test query", top_k=5)
        
        assert results == []
        mock_repository.list_all.assert_called_once()
        mock_embedding_service.embed_texts.assert_not_called()

    def test_search_returns_top_k_results(
        self, query_service, mock_repository, mock_embedding_service, sample_documents
    ):
        """Test search returns correct number of results based on top_k."""
        mock_repository.list_all.return_value = sample_documents
        
        # Query embedding similar to doc3
        query_emb = np.array([0.7071, 0.7071, 0.0], dtype=np.float32)
        mock_embedding_service.embed_texts.return_value = query_emb.reshape(1, -1)
        
        results = query_service.search("test query", top_k=2)
        
        assert len(results) == 2
        assert all(isinstance(r, DocumentQueryResult) for r in results)
        mock_repository.list_all.assert_called_once()
        mock_embedding_service.embed_texts.assert_called_once_with(["test query"])

    def test_search_ranks_by_similarity(
        self, query_service, mock_repository, mock_embedding_service, sample_documents
    ):
        """Test search ranks documents by cosine similarity."""
        mock_repository.list_all.return_value = sample_documents
        
        # Query embedding identical to doc1
        query_emb = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        mock_embedding_service.embed_texts.return_value = query_emb.reshape(1, -1)
        
        results = query_service.search("test query", top_k=3)
        
        # Doc1 should be first (perfect match)
        assert results[0].id == 1
        assert results[0].score > 0.99  # Close to 1.0
        # Scores should be in descending order
        assert results[0].score >= results[1].score >= results[2].score

    def test_search_uses_default_top_k_from_settings(
        self, query_service, mock_repository, mock_embedding_service, sample_documents
    ):
        """Test search uses default top_k when not specified."""
        mock_repository.list_all.return_value = sample_documents
        
        query_emb = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        mock_embedding_service.embed_texts.return_value = query_emb.reshape(1, -1)
        
        results = query_service.search("test query", top_k=None)
        
        # Should return results (at least 1)
        assert len(results) >= 1
        assert all(isinstance(r, DocumentQueryResult) for r in results)

    def test_search_limits_top_k_to_document_count(
        self, query_service, mock_repository, mock_embedding_service, sample_documents
    ):
        """Test search limits top_k to available document count."""
        mock_repository.list_all.return_value = sample_documents
        
        query_emb = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        mock_embedding_service.embed_texts.return_value = query_emb.reshape(1, -1)
        
        # Request more than available
        results = query_service.search("test query", top_k=100)
        
        # Should only return 3 documents
        assert len(results) == 3

    def test_search_result_structure(
        self, query_service, mock_repository, mock_embedding_service, sample_documents
    ):
        """Test search results have correct structure."""
        mock_repository.list_all.return_value = sample_documents
        
        query_emb = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        mock_embedding_service.embed_texts.return_value = query_emb.reshape(1, -1)
        
        results = query_service.search("test query", top_k=1)
        
        result = results[0]
        assert hasattr(result, 'id')
        assert hasattr(result, 'title')
        assert hasattr(result, 'score')
        assert isinstance(result.id, int)
        assert isinstance(result.title, str)
        assert isinstance(result.score, float)

    def test_cosine_similarities_method(self, query_service):
        """Test _cosine_similarities calculates correct values."""
        # Create orthogonal vectors
        doc_embeddings = np.array([
            [1.0, 0.0],
            [0.0, 1.0],
            [0.7071, 0.7071]
        ], dtype=np.float32)
        
        query_embedding = np.array([1.0, 0.0], dtype=np.float32)
        
        similarities = query_service._cosine_similarities(doc_embeddings, query_embedding)
        
        assert len(similarities) == 3
        assert np.isclose(similarities[0], 1.0, atol=1e-5)  # Parallel vectors
        assert np.isclose(similarities[1], 0.0, atol=1e-5)  # Orthogonal vectors
        assert 0.6 < similarities[2] < 0.8  # 45-degree angle

    def test_cosine_similarities_with_normalized_vectors(self, query_service):
        """Test _cosine_similarities with pre-normalized vectors."""
        # Normalized vectors
        doc_embeddings = np.array([[0.6, 0.8]], dtype=np.float32)
        query_embedding = np.array([0.6, 0.8], dtype=np.float32)
        
        similarities = query_service._cosine_similarities(doc_embeddings, query_embedding)
        
        # Same normalized vectors should have similarity of 1.0
        assert np.isclose(similarities[0], 1.0, atol=1e-5)

    def test_search_with_single_document(
        self, query_service, mock_repository, mock_embedding_service
    ):
        """Test search with only one document."""
        single_doc = DocumentModel(
            id=1,
            title="Only Document",
            content="Only content",
            embedding=np.array([1.0, 0.0, 0.0], dtype=np.float32).tobytes()
        )
        mock_repository.list_all.return_value = [single_doc]
        
        query_emb = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        mock_embedding_service.embed_texts.return_value = query_emb.reshape(1, -1)
        
        results = query_service.search("test", top_k=5)
        
        assert len(results) == 1
        assert results[0].id == 1
        assert results[0].title == "Only Document"
