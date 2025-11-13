"""Integration tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient
import numpy as np

from app.infrastructure.persistence.models.document import DocumentModel


class TestDocumentsEndpoints:
    """Test suite for /api/v1/documents endpoints."""

    def test_create_documents_success(self, client, mock_embedding_service):
        """Test successful creation of documents."""
        # Configure embeddings for this test
        mock_embeddings = np.array([
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6]
        ], dtype=np.float32)
        mock_embedding_service.embed_texts.return_value = mock_embeddings
        
        payload = [
            {
                "title": "First Document",
                "content": "This is the first document content"
            },
            {
                "title": "Second Document",
                "content": "This is the second document content"
            }
        ]
        
        response = client.post("/api/v1/documents/", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "First Document"
        assert data[0]["content"] == "This is the first document content"
        assert data[1]["title"] == "Second Document"
        assert "id" in data[0]
        assert "id" in data[1]
        # Embedding should not be in response
        assert "embedding" not in data[0]

    def test_create_single_document(self, client, mock_embedding_service):
        """Test creating a single document."""
        mock_embeddings = np.array([[0.1, 0.2, 0.3]], dtype=np.float32)
        mock_embedding_service.embed_texts.return_value = mock_embeddings
        
        payload = [
            {
                "title": "Solo Document",
                "content": "Just one document"
            }
        ]
        
        response = client.post("/api/v1/documents/", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Solo Document"

    def test_list_documents_empty(self, client):
        """Test listing documents when database is empty."""
        response = client.get("/api/v1/documents/")
        
        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_list_documents_returns_all(self, client, mock_embedding_service):
        """Test listing all documents after creation."""
        # Configure embeddings
        mock_embeddings = np.array([
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6],
            [0.7, 0.8, 0.9]
        ], dtype=np.float32)
        mock_embedding_service.embed_texts.return_value = mock_embeddings
        
        # Create some documents
        payload = [
            {"title": f"Doc {i}", "content": f"Content {i}"}
            for i in range(3)
        ]
        client.post("/api/v1/documents/", json=payload)
        
        # List documents
        response = client.get("/api/v1/documents/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all("id" in doc for doc in data)
        assert all("title" in doc for doc in data)
        assert all("content" in doc for doc in data)

    def test_get_document_by_id_success(self, client, mock_embedding_service):
        """Test getting a specific document by ID."""
        # Configure embeddings
        mock_embeddings = np.array([[0.1, 0.2, 0.3]], dtype=np.float32)
        mock_embedding_service.embed_texts.return_value = mock_embeddings
        
        # Create a document
        payload = [{"title": "Target Document", "content": "Target content"}]
        create_response = client.post("/api/v1/documents/", json=payload)
        created_doc = create_response.json()[0]
        doc_id = created_doc["id"]
        
        # Get document by ID
        response = client.get(f"/api/v1/documents/{doc_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == doc_id
        assert data["title"] == "Target Document"
        assert data["content"] == "Target content"

    def test_get_document_by_id_not_found(self, client):
        """Test getting a non-existent document returns 404."""
        response = client.get("/api/v1/documents/9999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_create_documents_with_special_characters(self, client, mock_embedding_service):
        """Test creating documents with special characters."""
        mock_embeddings = np.array([[0.1, 0.2, 0.3]], dtype=np.float32)
        mock_embedding_service.embed_texts.return_value = mock_embeddings
        
        payload = [
            {
                "title": "Document with émojis 🎉",
                "content": "Content with special chars: <>&\"\n\t"
            }
        ]
        
        response = client.post("/api/v1/documents/", json=payload)
        
        assert response.status_code == 201
        data = response.json()[0]
        assert data["title"] == "Document with émojis 🎉"


class TestQueryEndpoints:
    """Test suite for /api/v1/query endpoints."""

    def test_query_empty_database(self, client, mock_embedding_service):
        """Test querying when database is empty."""
        query_embedding = np.array([0.1, 0.2, 0.3], dtype=np.float32)
        mock_embedding_service.embed_texts.return_value = query_embedding.reshape(1, -1)
        
        response = client.get(
            "/api/v1/query/",
            params={"query": "test query", "top_k": 5}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "test query"
        assert data["results"] == []

    def test_query_returns_results(self, client, mock_embedding_service):
        """Test querying returns matching documents."""
        # Create documents
        create_embeddings = np.array([
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.7071, 0.7071, 0.0]
        ], dtype=np.float32)
        mock_embedding_service.embed_texts.return_value = create_embeddings
        
        payload = [
            {"title": "Python Programming", "content": "Learn Python"},
            {"title": "JavaScript Guide", "content": "Learn JS"},
            {"title": "Web Development", "content": "Full stack"}
        ]
        client.post("/api/v1/documents/", json=payload)
        
        # Query documents
        query_embedding = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        mock_embedding_service.embed_texts.return_value = query_embedding.reshape(1, -1)
        
        response = client.get(
            "/api/v1/query/",
            params={"query": "python programming", "top_k": 2}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "python programming"
        assert len(data["results"]) == 2
        assert all("id" in r for r in data["results"])
        assert all("title" in r for r in data["results"])
        assert all("score" in r for r in data["results"])

    def test_query_results_ordered_by_score(self, client, mock_embedding_service):
        """Test that query results are ordered by similarity score."""
        # Create documents
        create_embeddings = np.array([
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0]
        ], dtype=np.float32)
        mock_embedding_service.embed_texts.return_value = create_embeddings
        
        payload = [
            {"title": "Exact Match", "content": "Content A"},
            {"title": "Different", "content": "Content B"}
        ]
        client.post("/api/v1/documents/", json=payload)
        
        # Query documents
        query_embedding = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        mock_embedding_service.embed_texts.return_value = query_embedding.reshape(1, -1)
        
        response = client.get(
            "/api/v1/query/",
            params={"query": "find exact match", "top_k": 2}
        )
        
        data = response.json()
        results = data["results"]
        # Scores should be in descending order
        assert results[0]["score"] >= results[1]["score"]

    def test_query_without_top_k_uses_default(self, client, mock_embedding_service):
        """Test that query uses default top_k when not specified."""
        # Create document
        create_embeddings = np.array([[0.1, 0.2, 0.3]], dtype=np.float32)
        mock_embedding_service.embed_texts.return_value = create_embeddings
        
        payload = [{"title": "Doc", "content": "Content"}]
        client.post("/api/v1/documents/", json=payload)
        
        # Query without top_k
        query_embedding = np.array([0.1, 0.2, 0.3], dtype=np.float32)
        mock_embedding_service.embed_texts.return_value = query_embedding.reshape(1, -1)
        
        response = client.get(
            "/api/v1/query/",
            params={"query": "test"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert len(data["results"]) >= 0

    def test_query_respects_top_k_limit(self, client, mock_embedding_service):
        """Test that query returns at most top_k results."""
        # Create documents
        create_embeddings = np.random.randn(5, 3).astype(np.float32)
        mock_embedding_service.embed_texts.return_value = create_embeddings
        
        payload = [
            {"title": f"Document {i}", "content": f"Content {i}"}
            for i in range(5)
        ]
        client.post("/api/v1/documents/", json=payload)
        
        # Query with top_k=3
        query_embedding = np.random.randn(3).astype(np.float32)
        mock_embedding_service.embed_texts.return_value = query_embedding.reshape(1, -1)
        
        response = client.get(
            "/api/v1/query/",
            params={"query": "find documents", "top_k": 3}
        )
        
        data = response.json()
        assert len(data["results"]) == 3
