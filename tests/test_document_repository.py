"""Tests for DocumentRepository."""
import pytest
from sqlalchemy.orm import Session

from app.infrastructure.persistence.repositories.document_repository import DocumentRepository
from app.infrastructure.persistence.models.document import DocumentModel


class TestDocumentRepository:
    """Test suite for DocumentRepository class."""

    @pytest.fixture
    def repository(self, db_session: Session):
        """Create a DocumentRepository instance with test database."""
        return DocumentRepository(db=db_session)

    @pytest.fixture
    def sample_document_data(self):
        """Create sample document data."""
        return {
            "title": "Test Document",
            "content": "This is test content",
            "embedding": b'\x00' * 1536  # Mock embedding bytes
        }

    def test_create_document(self, repository, sample_document_data):
        """Test creating a single document."""
        doc = DocumentModel(**sample_document_data)
        
        created_doc = repository.create(doc)
        
        assert created_doc.id is not None
        assert created_doc.title == sample_document_data["title"]
        assert created_doc.content == sample_document_data["content"]
        assert created_doc.embedding == sample_document_data["embedding"]

    def test_create_document_persists_to_db(self, repository, db_session, sample_document_data):
        """Test that created document is persisted in database."""
        doc = DocumentModel(**sample_document_data)
        
        created_doc = repository.create(doc)
        doc_id = created_doc.id
        
        # Query directly from database
        db_doc = db_session.query(DocumentModel).filter(DocumentModel.id == doc_id).first()
        assert db_doc is not None
        assert db_doc.title == sample_document_data["title"]

    def test_create_many_documents(self, repository):
        """Test creating multiple documents."""
        docs = [
            DocumentModel(
                title=f"Document {i}",
                content=f"Content {i}",
                embedding=b'\x00' * 1536
            )
            for i in range(3)
        ]
        
        created_docs = repository.create_many(docs)
        
        assert len(created_docs) == 3
        for i, doc in enumerate(created_docs):
            assert doc.id is not None
            assert doc.title == f"Document {i}"
            assert doc.content == f"Content {i}"

    def test_create_many_empty_list(self, repository):
        """Test creating an empty list of documents."""
        created_docs = repository.create_many([])
        
        assert created_docs == []

    def test_list_all_empty(self, repository):
        """Test listing all documents when database is empty."""
        documents = repository.list_all()
        
        assert documents == []

    def test_list_all_returns_all_documents(self, repository):
        """Test listing all documents returns all persisted documents."""
        # Create some documents
        docs = [
            DocumentModel(
                title=f"Doc {i}",
                content=f"Content {i}",
                embedding=b'\x00' * 1536
            )
            for i in range(5)
        ]
        repository.create_many(docs)
        
        all_docs = repository.list_all()
        
        assert len(all_docs) == 5
        assert all(isinstance(doc, DocumentModel) for doc in all_docs)

    def test_get_by_id_existing_document(self, repository, sample_document_data):
        """Test getting a document by existing ID."""
        doc = DocumentModel(**sample_document_data)
        created_doc = repository.create(doc)
        doc_id = created_doc.id
        
        retrieved_doc = repository.get_by_id(doc_id)
        
        assert retrieved_doc is not None
        assert retrieved_doc.id == doc_id
        assert retrieved_doc.title == sample_document_data["title"]
        assert retrieved_doc.content == sample_document_data["content"]

    def test_get_by_id_non_existing_document(self, repository):
        """Test getting a document by non-existing ID returns None."""
        retrieved_doc = repository.get_by_id(9999)
        
        assert retrieved_doc is None

    def test_get_by_id_after_create_many(self, repository):
        """Test getting specific document after creating many."""
        docs = [
            DocumentModel(
                title=f"Document {i}",
                content=f"Content {i}",
                embedding=b'\x00' * 1536
            )
            for i in range(3)
        ]
        created_docs = repository.create_many(docs)
        target_id = created_docs[1].id
        
        retrieved_doc = repository.get_by_id(target_id)
        
        assert retrieved_doc is not None
        assert retrieved_doc.id == target_id
        assert retrieved_doc.title == "Document 1"

    def test_create_many_maintains_order(self, repository):
        """Test that create_many maintains the order of documents."""
        titles = ["First", "Second", "Third"]
        docs = [
            DocumentModel(
                title=title,
                content=f"Content for {title}",
                embedding=b'\x00' * 1536
            )
            for title in titles
        ]
        
        created_docs = repository.create_many(docs)
        
        for i, (created, original_title) in enumerate(zip(created_docs, titles)):
            assert created.title == original_title

    def test_list_all_returns_fresh_data(self, repository, sample_document_data):
        """Test that list_all returns fresh data from database."""
        # Create initial document
        doc = DocumentModel(**sample_document_data)
        repository.create(doc)
        
        # Get initial list
        docs1 = repository.list_all()
        initial_count = len(docs1)
        
        # Create another document
        doc2 = DocumentModel(
            title="Another Document",
            content="More content",
            embedding=b'\x00' * 1536
        )
        repository.create(doc2)
        
        # Get updated list
        docs2 = repository.list_all()
        
        assert len(docs2) == initial_count + 1

    def test_documents_have_auto_increment_ids(self, repository):
        """Test that documents get auto-incremented IDs."""
        docs = [
            DocumentModel(
                title=f"Doc {i}",
                content=f"Content {i}",
                embedding=b'\x00' * 1536
            )
            for i in range(3)
        ]
        
        created_docs = repository.create_many(docs)
        ids = [doc.id for doc in created_docs]
        
        # All IDs should be unique
        assert len(set(ids)) == len(ids)
        # IDs should be positive integers
        assert all(id > 0 for id in ids)
