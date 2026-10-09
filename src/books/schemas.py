from pydantic import BaseModel
import uuid
from datetime import date, datetime


# 1. Renamed this from Book to BookResponseModel to prevent naming conflicts
class BookResponseModel(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime

    # This allows Pydantic to read data seamlessly from SQLModel database objects
    model_config = {"from_attributes": True}


class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
