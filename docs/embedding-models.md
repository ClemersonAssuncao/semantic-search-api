# Embedding Models

This document explains the embedding models that can be used in the Semantic Search API and how to configure them.

## Current Model

The application currently uses **all-MiniLM-L6-v2** as the default embedding model. This model is provided by the `sentence-transformers` library and offers a good balance between performance and accuracy for semantic search tasks.

## Available Models

The application supports any model from the [Sentence Transformers](https://www.sbert.net/) library. Here are some recommended options:

### Lightweight Models (Faster, Lower Memory)

- **all-MiniLM-L6-v2** (default)
  - Dimensions: 384
  - Performance: ~14k sentences/sec
  - Use case: General purpose, good balance
  
- **all-MiniLM-L12-v2**
  - Dimensions: 384
  - Performance: ~7k sentences/sec
  - Use case: Slightly better accuracy than L6

### High-Performance Models (Better Accuracy, Slower)

- **all-mpnet-base-v2**
  - Dimensions: 768
  - Performance: ~2.8k sentences/sec
  - Use case: Best overall quality for semantic search

- **multi-qa-mpnet-base-dot-v1**
  - Dimensions: 768
  - Performance: ~2.8k sentences/sec
  - Use case: Optimized for question-answering tasks

### Multilingual Models

- **paraphrase-multilingual-MiniLM-L12-v2**
  - Dimensions: 384
  - Performance: ~7k sentences/sec
  - Languages: 50+ languages
  - Use case: Multi-language semantic search

- **paraphrase-multilingual-mpnet-base-v2**
  - Dimensions: 768
  - Performance: ~2.5k sentences/sec
  - Languages: 50+ languages
  - Use case: Best quality for multilingual scenarios

## How to Change the Model

There are two ways to configure the embedding model in your application:

### Option 1: Environment Variable (Recommended)

The application is configured to read settings from a `.env` file automatically using `pydantic_settings`.

1. Create a `.env` file in the root directory of the project (if it doesn't exist)
2. Add the following line with your desired model (use uppercase with underscores):

```env
EMBEDDING_MODEL_NAME=all-mpnet-base-v2
```

3. Restart the application

**Note**: The environment variable name must be in uppercase: `EMBEDDING_MODEL_NAME` maps to the `embedding_model_name` setting.

### Option 2: Direct Configuration

Edit the `app/infrastructure/settings.py` file and change the default value:

```python
class Settings(BaseSettings):
    app_name: str = "Semantic Search API"
    database_url: str = "sqlite:///./documents.db"
    embedding_model_name: str = "all-mpnet-base-v2"  # Change this line
    default_query_top_k: int = 5
```

**Note**: This method changes the default value. Environment variables in `.env` will override this setting.

## Important Considerations

### Model Consistency

⚠️ **Warning**: If you change the embedding model after indexing documents, you must **re-index all documents**. Different models produce different embedding vectors, and mixing embeddings from different models will result in poor search results.

### Storage Requirements

- Models with higher dimensions (768) require more storage space per document
- A 384-dimensional embedding uses ~1.5 KB per document
- A 768-dimensional embedding uses ~3 KB per document

### Performance Trade-offs

- **Lightweight models** (MiniLM-L6): Faster indexing and querying, suitable for large datasets
- **High-performance models** (mpnet): Better semantic understanding, best for accuracy-critical applications
- **Multilingual models**: Necessary for non-English content or cross-language search

## First-Time Model Download

When you start the application with a new model, `sentence-transformers` will automatically download it from HuggingFace. This only happens once:

- The model is cached locally in `~/.cache/torch/sentence_transformers/`
- Download size varies: 80-400 MB depending on the model
- Subsequent starts will use the cached model

## Testing Different Models

To experiment with different models:

1. Backup your current database: `cp documents.db documents.db.backup`
2. Change the model using one of the methods above
3. Delete the database to start fresh: `rm documents.db`
4. Restart the application
5. Re-index your documents
6. Compare search quality

## Additional Resources

- [Sentence Transformers Documentation](https://www.sbert.net/)
- [Model Performance Benchmarks](https://www.sbert.net/docs/pretrained_models.html)
- [HuggingFace Model Hub](https://huggingface.co/models?library=sentence-transformers)
