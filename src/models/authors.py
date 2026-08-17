from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class AuthorsOrm(Base):
    __tablename__ = "authors"

    full_name: Mapped[str]
    bio: Mapped[str | None]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    books: Mapped[list["BooksOrm"]] = relationship("BooksOrm", back_populates="author")
    user = relationship("UsersOrm")

    def __repr__(self) -> str:
        return f"<Author {self.full_name}>"