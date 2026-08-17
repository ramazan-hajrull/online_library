from datetime import datetime

from sqlalchemy import ForeignKey, String, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
#from src.models import BooksOrm


class ReviewsOrm(Base):
    __tablename__ = 'reviews'
    __table_args__ = (
        CheckConstraint("rating >= 0 AND rating <= 5", name="ck_review_rating_range"),
    )

    text: Mapped[str]
    rating: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))

    book: Mapped["BooksOrm"] = relationship("BooksOrm", back_populates="reviews")
    user = relationship("UsersOrm")

    def __repr__(self) -> str:
        return f"<Review book={self.book_id} user={self.user_id} rating={self.rating}>"