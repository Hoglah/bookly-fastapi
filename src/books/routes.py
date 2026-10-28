from fastapi import APIRouter, status, Depends
from src.books.schemas import (
    BookResponseModel,
    BookUpdateModel,
    BookCreateModel,
    BookDetailModel,
)
from src.db.main import get_session
from src.books.service import BookService
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import AccessTokenBearer
from src.auth.dependencies import RoleChecker
from src.errors import BookNotFound

books_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["admin", "user"])


@books_router.get(
    "/", response_model=List[BookResponseModel], dependencies=[Depends(role_checker)]
)
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    books = await book_service.get_all_books(session)
    return books


@books_router.get(
    "/user/{user_uid}",
    response_model=List[BookResponseModel],
    dependencies=[Depends(role_checker)],
)
async def get_user_book_submissions(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    books = await book_service.get_user_books(user_uid, session)
    return books


@books_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=BookResponseModel,
    dependencies=[Depends(role_checker)],
)
async def create_a_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    user_id = token_details.get("user")["user_uid"]
    new_book = await book_service.create_book(book_data, user_id, session)
    return new_book


@books_router.get(
    "/{book_uid}",
    response_model=BookDetailModel,
    dependencies=[Depends(role_checker)],
)
async def get_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    book = await book_service.get_book(book_uid, session)
    if not book:
        raise BookNotFound()
    return book


@books_router.patch(
    "/{book_uid}",
    response_model=BookResponseModel,
    dependencies=[Depends(role_checker)],
)
async def update_book(
    book_uid: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    if not updated_book:
        raise BookNotFound()
    return updated_book


@books_router.delete(
    "/{book_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(role_checker)],
)
async def delete_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    book_to_delete = await book_service.delete_book(book_uid, session)
    if book_to_delete is None:
        raise BookNotFound()
    else:
        return {"message": "Book deleted successfully"}
