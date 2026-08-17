from datetime import datetime
from typing import Literal, Annotated

from fastapi import Depends
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Query

from src.schemas.authors import Author


class BookBase(BaseModel):
    title: str
    description: str | None = None
    published_year: int | None = None


class BookCreate(BookBase):
    author_id: int


class BookUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    published_year: int | None = None


class Book(BookBase):
    id: int
    average_rating: float
    reviews_count: int
    cover_path: str | None = None
    file_path: str | None = None
    author_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
"""
class BookFilterParams(BaseModel):
    author_id: int | None = Query(default=None)
    min_rating: float | None = Query(default=None, ge=0, le=5)
    search: str | None = Query(default=None)
    sort_by: Literal[
        "created_at",
        "average_rating",
        "title",
    ] = Query(default="created_at")
    order: Literal["asc", "desc"] = Query(default="desc")


BookFilterDep = Annotated[BookFilterParams, Depends()]
"""

class BookFilterParams(BaseModel):
    author_id: int | None = None
    min_rating: float | None = Field(default=None, ge=0, le=5)
    search: str | None = None
    sort_by: Literal[
        "created_at",
        "average_rating",
        "title"
    ] = "created_at"
    order: Literal["asc", "desc"] = "desc"
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)