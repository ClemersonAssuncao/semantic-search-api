from fastapi import FastAPI




def create_app() -> FastAPI:
    app = FastAPI(title="My FastAPI Application")

    @app.get("/")
    async def read_root():
        return {"message": "Hello, World!"}


    return app


app = create_app()