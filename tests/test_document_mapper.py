"""Tests for DocumentMapper."""
import pytest
import numpy as np

from app.core.mappers.document_mapper import DocumentMapper
from app.api.schemas.document import DocumentCreate, DocumentRead
from app.infrastructure.persistence.models.document import DocumentModel


class TestDocumentMapper:
    """Test suite for DocumentMapper class."""

    @pytest.fixture
    def document_create_dto(self):
        """Create a sample DocumentCreate DTO."""
        return DocumentCreate(
            title="Test Document",
            content="This is the content of the test document"
        )

    @pytest.fixture
    def document_model(self):
        """Create a sample DocumentModel."""
        embedding = np.array([1.0, 2.0, 3.0], dtype=np.float32)
        return DocumentModel(
            id=1,
            title="Model Document",
            content="This is model content",
            embedding=embedding.tobytes()
        )

    @pytest.fixture
    def sample_embedding(self):
        """Create a sample numpy embedding."""
        return np.array([0.1, 0.2, 0.3, 0.4, 0.5], dtype=np.float32)

    def test_to_model_with_numpy_array(self, document_create_dto, sample_embedding):
        """Test converting DocumentCreate to DocumentModel with numpy array."""
        model = DocumentMapper.to_model(document_create_dto, sample_embedding)
        
        assert isinstance(model, DocumentModel)
        assert model.title == document_create_dto.title
        assert model.content == document_create_dto.content
        assert isinstance(model.embedding, bytes)
        # Verify we can reconstruct the embedding
        reconstructed = np.frombuffer(model.embedding, dtype=np.float32)
        np.testing.assert_array_equal(reconstructed, sample_embedding)

    def test_to_model_with_bytes(self, document_create_dto):
        """Test converting DocumentCreate to DocumentModel with bytes embedding."""
        embedding_bytes = np.array([1.0, 2.0, 3.0], dtype=np.float32).tobytes()
        
        model = DocumentMapper.to_model(document_create_dto, embedding_bytes)
        
        assert isinstance(model, DocumentModel)
        assert model.title == document_create_dto.title
        assert model.content == document_create_dto.content
        assert model.embedding == embedding_bytes

    def test_to_model_preserves_all_fields(self, sample_embedding):
        """Test that to_model preserves all fields from DTO."""
        dto = DocumentCreate(
            title="Complex Title with Symbols!@#",
            content="Complex content\nwith\nnewlines\tand\ttabs"
        )
        
        model = DocumentMapper.to_model(dto, sample_embedding)
        
        assert model.title == dto.title
        assert model.content == dto.content

    def test_to_model_with_empty_strings(self, sample_embedding):
        """Test to_model with empty title and content."""
        dto = DocumentCreate(title="", content="")
        
        model = DocumentMapper.to_model(dto, sample_embedding)
        
        assert model.title == ""
        assert model.content == ""
        assert isinstance(model.embedding, bytes)

    def test_to_model_with_unicode_characters(self, sample_embedding):
        """Test to_model with unicode characters."""
        dto = DocumentCreate(
            title="Título com acentuação",
            content="Conteúdo com émojis 🎉 e caracteres especiais ñ ü"
        )
        
        model = DocumentMapper.to_model(dto, sample_embedding)
        
        assert model.title == dto.title
        assert model.content == dto.content

    def test_to_read_basic(self, document_model):
        """Test converting DocumentModel to DocumentRead."""
        dto = DocumentMapper.to_read(document_model)
        
        assert isinstance(dto, DocumentRead)
        assert dto.id == document_model.id
        assert dto.title == document_model.title
        assert dto.content == document_model.content

    def test_to_read_does_not_include_embedding(self, document_model):
        """Test that to_read does not include embedding in the DTO."""
        dto = DocumentMapper.to_read(document_model)
        
        # DocumentRead should not have embedding field
        assert not hasattr(dto, 'embedding')
        # But should have all other fields
        assert hasattr(dto, 'id')
        assert hasattr(dto, 'title')
        assert hasattr(dto, 'content')

    def test_to_read_preserves_all_fields(self):
        """Test that to_read preserves all fields correctly."""
        model = DocumentModel(
            id=42,
            title="Important Document",
            content="Critical information",
            embedding=b'\x00' * 100
        )
        
        dto = DocumentMapper.to_read(model)
        
        assert dto.id == 42
        assert dto.title == "Important Document"
        assert dto.content == "Critical information"

    def test_to_read_with_special_characters(self):
        """Test to_read with special characters."""
        model = DocumentModel(
            id=1,
            title="Special: Title & Content",
            content="Content with <html> tags and \"quotes\"",
            embedding=b'\x00' * 100
        )
        
        dto = DocumentMapper.to_read(model)
        
        assert dto.title == model.title
        assert dto.content == model.content

    def test_round_trip_conversion(self, sample_embedding):
        """Test converting DTO -> Model -> DTO preserves data."""
        original_dto = DocumentCreate(
            title="Round Trip Test",
            content="This should survive the round trip"
        )
        
        # Convert to model
        model = DocumentMapper.to_model(original_dto, sample_embedding)
        model.id = 1  # Simulate database assignment
        
        # Convert back to read DTO
        read_dto = DocumentMapper.to_read(model)
        
        # Verify data integrity (excluding id which is added)
        assert read_dto.title == original_dto.title
        assert read_dto.content == original_dto.content
        assert read_dto.id == 1

    def test_to_model_with_large_embedding(self, document_create_dto):
        """Test to_model with large embedding vector."""
        # Create a large embedding (e.g., 1536 dimensions like OpenAI)
        large_embedding = np.random.randn(1536).astype(np.float32)
        
        model = DocumentMapper.to_model(document_create_dto, large_embedding)
        
        assert isinstance(model.embedding, bytes)
        reconstructed = np.frombuffer(model.embedding, dtype=np.float32)
        assert len(reconstructed) == 1536
        np.testing.assert_array_equal(reconstructed, large_embedding)

    def test_to_model_with_normalized_embedding(self, document_create_dto):
        """Test to_model with normalized embedding."""
        # Create normalized embedding
        embedding = np.array([0.6, 0.8], dtype=np.float32)  # norm = 1.0
        
        model = DocumentMapper.to_model(document_create_dto, embedding)
        
        reconstructed = np.frombuffer(model.embedding, dtype=np.float32)
        norm = np.linalg.norm(reconstructed)
        assert np.isclose(norm, 1.0)

    def test_mapper_is_stateless(self, document_create_dto, sample_embedding):
        """Test that mapper methods are stateless and can be called multiple times."""
        model1 = DocumentMapper.to_model(document_create_dto, sample_embedding)
        model2 = DocumentMapper.to_model(document_create_dto, sample_embedding)
        
        # Should create independent instances
        assert model1 is not model2
        assert model1.title == model2.title
        assert model1.content == model2.content
