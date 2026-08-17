from pydantic import BaseModel, ConfigDict

from src.models import AuthorsOrm
from src.schemas.books import Book


class Favorite(BaseModel):
    id: int
    book_id: int

    model_config = ConfigDict(from_attributes=True)

class AuthorShort(BaseModel):
    full_name: str

    model_config = ConfigDict(from_attributes=True)

class FavoriteBookOut(BaseModel):
    id: int
    title: str
    author: AuthorShort

    model_config = ConfigDict(from_attributes=True)