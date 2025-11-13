import logging
from fastapi import FastAPI

from app.api.v1 import documents, query
from app.infrastructure.persistence.db.base import Base
from app.infrastructure.persistence.db.session import engine
from app.core.logging import setup_logging
from app.infrastructure.settings import settings

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    # Configure logging
    setup_logging(settings.log_level)
    
    logger.info(f"Starting {settings.app_name}")
    logger.debug(f"Log level set to: {settings.log_level}")
    
    app = FastAPI(title="Semantic Search API")

    # Lembrar de usar migrations depois, alembic
    logger.info("Creating database tables")
    Base.metadata.create_all(bind=engine)

    logger.info("Registering API routers")
    app.include_router(documents.router)
    app.include_router(query.router)

    logger.info(f"{settings.app_name} startup complete")
    return app


app = create_app()