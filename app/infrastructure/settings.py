from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Semantic Search API"
    database_url: str = "sqlite:///./documents.db"
    embedding_model_name: str = "all-MiniLM-L6-v2"
    default_query_top_k: int = 5

    class Config:
        env_file = ".env"


settings = Settings()