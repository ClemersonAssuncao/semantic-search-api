from fastapi import FastAPI

from app.api.v1 import documents, query
from app.infrastructure.persistence.db.base import Base
from app.infrastructure.persistence.db.session import engine


def create_app() -> FastAPI:
    app = FastAPI(title="Semantic Search API")

    # Lembrar de usar migrations depois, alembic
    Base.metadata.create_all(bind=engine)

    app.include_router(documents.router)
    app.include_router(query.router)

    return app


app = create_app()