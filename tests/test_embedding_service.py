"""Tests for EmbeddingService."""
import pytest
import numpy as np
from unittest.mock import Mock, patch

from app.core.services.embedding_service import EmbeddingService, get_embedding_service


class TestEmbeddingService:
    """Test suite for EmbeddingService class."""

    @patch('app.core.services.embedding_service.SentenceTransformer')
    def test_init_with_default_model(self, mock_transformer):
        """Test initialization with default model from settings."""
        mock_model_instance = Mock()
        mock_transformer.return_value = mock_model_instance
        
        service = EmbeddingService()
        
        assert service._model == mock_model_instance
        mock_transformer.assert_called_once()

    @patch('app.core.services.embedding_service.SentenceTransformer')
    def test_init_with_custom_model(self, mock_transformer):
        """Test initialization with custom model name."""
        mock_model_instance = Mock()
        mock_transformer.return_value = mock_model_instance
        custom_model = "custom-model-name"
        
        service = EmbeddingService(model_name=custom_model)
        
        assert service.model_name == custom_model
        assert service._model == mock_model_instance

    @patch('app.core.services.embedding_service.SentenceTransformer')
    def test_model_property(self, mock_transformer):
        """Test model property getter."""
        mock_model_instance = Mock()
        mock_transformer.return_value = mock_model_instance
        
        service = EmbeddingService()
        model = service.model
        
        assert model == mock_model_instance

    @patch('app.core.services.embedding_service.SentenceTransformer')
    def test_embed_texts_single_text(self, mock_transformer):
        """Test embedding a single text."""
        mock_model = Mock()
        # Simulate model output
        mock_embeddings = np.array([[1.0, 2.0, 3.0]], dtype=np.float32)
        mock_model.encode.return_value = mock_embeddings
        mock_transformer.return_value = mock_model
        
        service = EmbeddingService()
        texts = ["Hello world"]
        
        result = service.embed_texts(texts)
        
        assert result.shape == (1, 3)
        assert result.dtype == np.float32
        # Check if embeddings are normalized
        norm = np.linalg.norm(result[0])
        assert np.isclose(norm, 1.0, atol=1e-5)
        mock_model.encode.assert_called_once_with(texts, convert_to_numpy=True)

    @patch('app.core.services.embedding_service.SentenceTransformer')
    def test_embed_texts_multiple_texts(self, mock_transformer):
        """Test embedding multiple texts."""
        mock_model = Mock()
        mock_embeddings = np.array([
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0]
        ], dtype=np.float32)
        mock_model.encode.return_value = mock_embeddings
        mock_transformer.return_value = mock_model
        
        service = EmbeddingService()
        texts = ["First text", "Second text", "Third text"]
        
        result = service.embed_texts(texts)
        
        assert result.shape == (3, 3)
        assert result.dtype == np.float32
        # Check if all embeddings are normalized
        for i in range(3):
            norm = np.linalg.norm(result[i])
            assert np.isclose(norm, 1.0, atol=1e-5)

    @patch('app.core.services.embedding_service.SentenceTransformer')
    def test_embed_texts_normalization(self, mock_transformer):
        """Test that embeddings are properly normalized."""
        mock_model = Mock()
        # Create embeddings with known norm
        mock_embeddings = np.array([[3.0, 4.0]], dtype=np.float32)  # norm = 5.0
        mock_model.encode.return_value = mock_embeddings
        mock_transformer.return_value = mock_model
        
        service = EmbeddingService()
        result = service.embed_texts(["test"])
        
        # Expected normalized values: [3/5, 4/5] = [0.6, 0.8]
        expected = np.array([[0.6, 0.8]], dtype=np.float32)
        np.testing.assert_array_almost_equal(result, expected, decimal=5)

    @patch('app.core.services.embedding_service.SentenceTransformer')
    def test_embed_texts_empty_list(self, mock_transformer):
        """Test embedding an empty list of texts."""
        mock_model = Mock()
        mock_embeddings = np.array([], dtype=np.float32).reshape(0, 384)
        mock_model.encode.return_value = mock_embeddings
        mock_transformer.return_value = mock_model
        
        service = EmbeddingService()
        result = service.embed_texts([])
        
        assert result.shape[0] == 0
        assert result.dtype == np.float32

    def test_get_embedding_service_singleton(self):
        """Test that get_embedding_service returns cached instance."""
        # Clear cache first
        get_embedding_service.cache_clear()
        
        with patch('app.core.services.embedding_service.SentenceTransformer'):
            service1 = get_embedding_service()
            service2 = get_embedding_service()
            
            assert service1 is service2
