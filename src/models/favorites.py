from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
#from src.models import BooksOrm, UsersOrm


class FavoritesOrm(Base):
    __tablename__ = "favorites"
    __table_args__ = (
        UniqueConstraint("user_id", "book_id"),
    )

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    book: Mapped["BooksOrm"] = relationship("BooksOrm")
    user: Mapped["UsersOrm"] = relationship("UsersOrm")