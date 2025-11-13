# Docker Usage Guide

## Building the Image

```bash
docker build -t semantic-search-api .
```

## Running with Docker Run

### Basic Usage
```bash
docker run -p 8000:8000 semantic-search-api
```

### With Environment Variables
```bash
docker run -p 8000:8000 \
  -e LOG_LEVEL=DEBUG \
  -e DEFAULT_QUERY_TOP_K=10 \
  -e EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2 \
  -e APP_NAME="My Custom API" \
  semantic-search-api
```

### With Volume for Database Persistence
```bash
docker run -p 8000:8000 \
  -e LOG_LEVEL=INFO \
  -v $(pwd)/data:/app/data \
  -e DATABASE_URL=sqlite:///./data/documents.db \
  semantic-search-api
```

## Running with Docker Compose

### Start the service
```bash
docker-compose up -d
```

### View logs
```bash
docker-compose logs -f
```

### Stop the service
```bash
docker-compose down
```

## Available Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | `Semantic Search API` | Application name |
| `DATABASE_URL` | `sqlite:///./documents.db` | Database connection URL |
| `EMBEDDING_MODEL_NAME` | `all-MiniLM-L6-v2` | Sentence transformer model name |
| `DEFAULT_QUERY_TOP_K` | `5` | Default number of results to return |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |

## Examples

### Development Mode (Debug Logging)
```bash
docker run -p 8000:8000 -e LOG_LEVEL=DEBUG semantic-search-api
```

### Production Mode (Error Logging Only)
```bash
docker run -p 8000:8000 -e LOG_LEVEL=ERROR semantic-search-api
```

### Custom Model
```bash
docker run -p 8000:8000 \
  -e EMBEDDING_MODEL_NAME=paraphrase-MiniLM-L6-v2 \
  semantic-search-api
```

## API Access

Once running, access the API at:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
