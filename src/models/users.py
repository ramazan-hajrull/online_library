from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
#from src.models import BooksOrm


class UsersOrm(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    #is_active: Mapped[bool]
    is_blocked: Mapped[bool] = mapped_column(default=False)

    """
    books: Mapped[list["BooksOrm"]] = relationship(
        "BooksOrm",
        back_populates="author"
    )
    """
    favorites: Mapped[list["BooksOrm"]] = relationship(
        "BooksOrm",
        secondary="favorites",
        back_populates="users"
    )

    role = relationship("RolesOrm")