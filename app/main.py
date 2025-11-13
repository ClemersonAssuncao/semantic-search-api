from fastapi import FastAPI

from app.api.v1 import documents



def create_app() -> FastAPI:
    app = FastAPI(title="My FastAPI Application")

    app.include_router(documents.router)

    return app


app = create_app()