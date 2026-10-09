from fastapi import FastAPI
from src.books.routes import books_router
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    print("server is starting...")
    await init_db()
    yield
    print("server has been stopped")


version = "v1"

app = FastAPI(
    title="Bookly API",
    description="A simple API for managing books",
    version=version,
    lifespan=life_span,
)
app.include_router(books_router, prefix=f"/api/{version}/books", tags=["books"])
