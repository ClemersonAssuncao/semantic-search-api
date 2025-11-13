from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Semantic Search API"
    database_url: str = "sqlite:///./documents.db"

    class Config:
        env_file = ".env"


settings = Settings()