from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReviewBase(BaseModel):
    rating: float = Field(ge=0, le=5)
    text: str | None = None

class ReviewAddRequest(ReviewBase):
    pass

class ReviewAdd(ReviewBase):
    book_id: int
    user_id: int

class ReviewUpdate(BaseModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    text: str | None = None

class Review(ReviewBase):
    id: int
    user_id: int
    book_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)