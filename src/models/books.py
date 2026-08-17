from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class BooksOrm(Base):
    __tablename__ = 'books'

    title: Mapped[str]
    description: Mapped[str | None]
    published_year: Mapped[int | None]
    average_rating: Mapped[float] = mapped_column(default=0.0)
    reviews_count: Mapped[int] = mapped_column(default=0)
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'))
    genre_id: Mapped[int | None] = mapped_column(ForeignKey('genres.id'))
    cover_path: Mapped[str | None]
    file_path: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    reviews: Mapped[list['ReviewsOrm']] = relationship("ReviewsOrm", back_populates='book')
    author: Mapped['AuthorsOrm'] = relationship("AuthorsOrm", back_populates='books')
    users: Mapped[list["UsersOrm"]] = relationship(
        "UsersOrm",
        secondary="favorites",
        back_populates="favorites"
    )

    def __repr__(self) -> str:
        return f"Book {self.title}"