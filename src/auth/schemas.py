from pydantic import BaseModel, Field
from src.books.schemas import BookResponseModel
from src.reviews.schemas import ReviewModel
import uuid
from datetime import datetime
from typing import List


class UserCreateModel(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(..., min_length=3, max_length=50)
    username: str = Field(..., min_length=3, max_length=8)
    email: str = Field(..., json_schema_extra={"email": True}, max_length=40)
    password: str = Field(..., min_length=6)


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(..., exclude=True)
    created_at: datetime
    updated_at: datetime


class UserBookModel(UserModel):
    books: List[BookResponseModel]
    reviews: List[ReviewModel]


class UserLoginModel(BaseModel):
    email: str = Field(..., email=True, max_length=40)
    password: str = Field(..., min_length=6)


class EmailModel(BaseModel):
    addresses: List[str]


class PasswordRequest(BaseModel):
    email: str


class PasswordRestConfirmModel(BaseModel):
    new_password: str
    confirm_password: str
