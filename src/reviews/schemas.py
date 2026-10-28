from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from typing import Optional


class ReviewModel(BaseModel):
    uid: uuid.UUID
    book_uid: Optional[uuid.UUID]
    user_uid: Optional[uuid.UUID]
    rating: int = Field(lt=5)
    comment: str
    created_at: datetime
    updated_at: datetime


class ReviewCreateModel(BaseModel):
    rating: int = Field(lt=5)
    comment: str
