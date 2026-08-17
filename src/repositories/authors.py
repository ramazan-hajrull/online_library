from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.authors import AuthorsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import AuthorDataMapper


class AuthorsRepository(BaseRepository):
    model = AuthorsOrm
    mapper = AuthorDataMapper

