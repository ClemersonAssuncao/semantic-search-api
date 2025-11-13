# Testing Guide

## Overview

This application includes a comprehensive suite of unit and integration tests to ensure code quality and reliability.

## Test Structure

```
tests/
├── __init__.py                    # Test package
├── conftest.py                    # Shared pytest fixtures
├── pytest.ini                     # Pytest configuration
├── test_embedding_service.py      # EmbeddingService unit tests (8 tests)
├── test_query_service.py          # QueryService unit tests (9 tests)
├── test_document_repository.py    # DocumentRepository unit tests (13 tests)
├── test_document_mapper.py        # DocumentMapper unit tests (12 tests)
└── test_api_endpoints.py          # API integration tests (12 tests)
```

**Total: 54 tests** (42 unit tests + 12 integration tests)

## Test Types

### Unit Tests (42 tests)
Test individual components in isolation with mocked dependencies:
- **EmbeddingService** (8 tests): Model initialization, embedding generation, normalization
- **QueryService** (9 tests): Search logic, ranking, cosine similarity calculations
- **DocumentRepository** (13 tests): Database CRUD operations
- **DocumentMapper** (12 tests): DTO to Model conversions and vice versa

### Integration Tests (12 tests)
Test complete API endpoints with real HTTP requests:
- **Documents Endpoints** (7 tests): POST, GET list, GET by ID with database operations
- **Query Endpoints** (5 tests): Semantic search with embedding generation and ranking

Integration tests use:
- FastAPI `TestClient` for HTTP requests
- In-memory SQLite database with `StaticPool`
- Mocked `EmbeddingService` to avoid model loading
- Dependency injection overrides for test isolation

## Running Tests

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install test dependencies directly:

```bash
pip install pytest pytest-cov pytest-mock httpx
```

### Run All Tests

```bash
pytest
```

Or using Python module syntax:

```bash
python -m pytest tests/ -v
```

### Run with Coverage

Generate an HTML coverage report:

```bash
pytest --cov=app --cov-report=html
```

View coverage in terminal:

```bash
pytest --cov=app --cov-report=term-missing
```

### Run Specific Tests

```bash
# Run a specific test file
pytest tests/test_embedding_service.py
python -m pytest tests/test_embedding_service.py -v

# Run only unit tests
pytest tests/test_embedding_service.py tests/test_query_service.py tests/test_document_repository.py tests/test_document_mapper.py

# Run only integration tests
pytest tests/test_api_endpoints.py

# Run a specific test class
pytest tests/test_query_service.py::TestQueryService

# Run a specific test method
pytest tests/test_document_repository.py::TestDocumentRepository::test_create_document
```

### Verbosity Options

```bash
pytest -v       # Verbose output
pytest -vv      # Very verbose output
pytest -vv -s   # Very verbose with print statements
```

## Pytest Configuration

The `pytest.ini` file configures:
- Test directory: `tests/`
- Naming patterns for test files, classes, and functions
- Default flags for execution
- Custom markers (unit, integration, slow)

## Key Fixtures

### `db_engine`
Creates a SQLite in-memory engine using `StaticPool` to ensure all connections share the same database instance during tests. This is critical for integration tests where FastAPI dependency injection needs access to the same database as test fixtures.

### `db_session`
Creates an in-memory database session for isolated tests. Each test function gets a fresh session that is automatically closed after the test completes.

### `mock_embedding_service`
Creates a mocked `EmbeddingService` that returns random embeddings without loading the actual SentenceTransformer model. This significantly speeds up tests and avoids downloading large model files.

### `client`
Creates a FastAPI `TestClient` with dependency overrides:
- Replaces `get_db` with test database session
- Replaces `get_embedding_service` with mocked service
- Configures FastAPI app with all API routers for integration testing

## Writing Tests

### Best Practices

1. **Isolation**: Each test should be independent and use in-memory database with `StaticPool`
2. **Mocking**: Mock external services (e.g., SentenceTransformer) to avoid slow model loading
3. **Fixtures**: Reuse common test configurations via `conftest.py`
4. **Naming**: Use descriptive names that explain what is being tested
5. **Structure**: Follow the Arrange-Act-Assert pattern
6. **Dependency Injection**: Override FastAPI dependencies in integration tests for proper isolation

### Test Structure Example

```python
def test_example():
    # Arrange: Set up test data
    mock_data = create_mock()
    
    # Act: Execute the action
    result = service.method(mock_data)
    
    # Assert: Verify the result
    assert result == expected
```

### Creating a New Test File

1. Create a new file in `tests/` with prefix `test_`
2. Import pytest and necessary modules
3. Create a test class with prefix `Test`
4. Write test methods with prefix `test_`

Example:

```python
"""Tests for MyService."""
import pytest
from app.services.my_service import MyService


class TestMyService:
    """Test suite for MyService class."""

    @pytest.fixture
    def service(self):
        """Create a MyService instance for testing."""
        return MyService()

    def test_method_returns_expected_value(self, service):
        """Test that method returns expected value."""
        result = service.method()
        assert result == "expected"
```

## Common Test Commands

```bash
# Run only unit tests (fast)
pytest -m unit

# Skip slow tests
pytest -m "not slow"

# Run with coverage and open HTML report
pytest --cov=app --cov-report=html && open htmlcov/index.html

# Run tests in parallel (requires pytest-xdist)
pytest -n auto
```

## Expected Metrics

- **Total Tests**: 54 (42 unit + 12 integration)
- **Code Coverage**: > 80%
- **Execution Time**: < 1 second (thanks to mocked services)
- **Success Rate**: 100%

## Continuous Integration

To integrate tests in CI/CD pipelines:

```yaml
# Example for GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest --cov=app --cov-report=xml
    
- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

## Troubleshooting

### Tests fail with import errors
Make sure you're in the project root directory and have installed all dependencies:
```bash
pip install -r requirements.txt
```

### Database errors in integration tests
Tests use an in-memory SQLite database with `StaticPool`. This ensures all connections share the same database instance. The pool configuration is critical for FastAPI dependency injection to work correctly in tests.

### Mocking issues
External services like `SentenceTransformer` are mocked via the `mock_embedding_service` fixture. For integration tests, the mock is automatically injected through FastAPI's dependency override system. For unit tests, configure the mock's return value in each test as needed.

### "no such table" errors
This typically indicates that `StaticPool` is not configured correctly in the database engine, or that the dependency override for `get_db` is not working. Check that `conftest.py` properly configures the test client with dependency overrides.

## Next Steps

- Add performance tests
- Implement end-to-end tests
- Add load testing
- Configure automated CI/CD execution
