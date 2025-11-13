# SEMANTIC SEARCH API

## Installation

1. Clone the repository:
```bash
git clone https://github.com/seu-usuario/semantic-search-api.git
cd semantic-search-api
```

2. Install dependencies:
```bash
python -m pip install -r requirements.txt
```

## Running the Application

To start the development server:

```bash
python -m uvicorn app.main:app --reload
```

The application will be available at:
- API: `http://localhost:8000`
- Swagger Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Documentation

- **[Embedding Models](docs/embedding-models.md)** - Learn about available embedding models and how to configure them for your semantic search needs
- **[Docker Guide](docs/docker.md)** - Complete guide for running the application in Docker containers with environment variable configuration