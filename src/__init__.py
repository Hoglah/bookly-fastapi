from fastapi import FastAPI
from src.books.routes import books_router
from src.auth.routes import auth_router
from src.reviews.routes import reviews_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from .errors import register_all_errors
from .middleware import register_middleware


@asynccontextmanager
async def life_span(app: FastAPI):
    print("server is starting...")
    await init_db()
    yield
    print("server has been stopped")


version = "v1"

app = FastAPI(
    title="Bookly",
    description="A REST API for managing books",
    version=version,
    docs_url=f"/api/{version}/docs",
    redoc_url=f"/api/{version}/redoc",
    contact={
        "email": "yaabirago1601@gmail.com",
    },
)

register_all_errors(app)
register_middleware(app)

app.include_router(books_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(reviews_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
