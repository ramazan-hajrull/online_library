from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class GenresOrm(Base):
    __tablename__ = 'genres'

    title: Mapped[str]
