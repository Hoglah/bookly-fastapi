from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.books.schemas import BookResponseModel, BookUpdateModel, BookCreateModel
from src.db.main import get_session
from src.books.service import BookService
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession

books_router = APIRouter()
book_service = BookService()


@books_router.get("/", response_model=List[BookResponseModel])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books


@books_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=BookResponseModel
)
async def create_a_book(
    book_data: BookCreateModel, session: AsyncSession = Depends(get_session)
) -> dict:
    new_book = await book_service.create_book(book_data, session)
    return new_book


@books_router.get("/{book_uid}", response_model=BookResponseModel)
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    book = await book_service.get_book(book_uid, session)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@books_router.patch("/{book_uid}", response_model=BookResponseModel)
async def update_book(
    book_uid: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


@books_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    book_to_delete = await book_service.delete_book(book_uid, session)
    if book_to_delete is None:
        raise HTTPException(status_code=404, detail="Book not found")
    else:
        return {"message": "Book deleted successfully"}
