"""Pytest configuration and shared fixtures."""
import pytest
from typing import Generator
from unittest.mock import Mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.infrastructure.persistence.db.base import Base
from app.api.v1 import documents, query


# Test database URL (using SQLite in memory)
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_engine():
    """Create a test database engine."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """Create a test database session."""
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db_engine
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def mock_embedding_service():
    """Create a mocked embedding service for tests."""
    import numpy as np
    mock = Mock()
    # Default behavior: return normalized embeddings
    mock.embed_texts.return_value = np.random.rand(1, 384).astype(np.float32)
    return mock


@pytest.fixture(scope="function")
def client(db_session, mock_embedding_service) -> Generator[TestClient, None, None]:
    """Create a test client with database dependency override."""
    from app.infrastructure.persistence.db.session import get_db
    from app.core.services.embedding_service import get_embedding_service
    
    # Create a minimal FastAPI app for testing
    app = FastAPI(title="Test Semantic Search API")
    app.include_router(documents.router)
    app.include_router(query.router)
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    # Override dependencies to use test database and mocked services
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_embedding_service] = lambda: mock_embedding_service
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

