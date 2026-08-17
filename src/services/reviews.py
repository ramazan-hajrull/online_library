from src.exceptions import (
    ReviewAlreadyExistsException,
    ReviewNotFoundException,
    CanEditOnlyOwnReviewException,
    CanDeleteOnlyOwnReviewException,
)
from src.models import UsersOrm
from src.schemas.reviews import ReviewAdd, ReviewAddRequest, ReviewUpdate
from src.services.base import BaseService
from src.tasks.tasks import notify_author, recompute_book_rating


class ReviewService(BaseService):
    async def list_reviews(self, book_id: int):
        return await self.db.reviews.get_all(book_id=book_id)

    async def create_review(self, book_id: int, payload: ReviewAddRequest, user_id: int):
        existing = await self.db.reviews.get_one_or_none(book_id=book_id, user_id=user_id)

        if existing:
            raise ReviewAlreadyExistsException

        review_data = ReviewAdd(
            book_id=book_id,
            user_id=user_id,
            **payload.model_dump()
        )
        review = await self.db.reviews.add(review_data)

        await self.db.commit()

        recompute_book_rating.delay(book_id)
        notify_author.delay(review.id)

        return review

    async def update_review(self, book_id: int, payload: ReviewUpdate, current_user: UsersOrm, review_id: int):
        review = await self.db.reviews.get_one_or_none(id=review_id)
        if review is None or review.book_id != book_id:
            raise ReviewNotFoundException
        if review.user_id != current_user.id and current_user.role.name != "ADMIN":
            raise CanEditOnlyOwnReviewException
        await self.db.reviews.edit(data=payload, exclude_unset=True, id=review_id)
        await self.db.commit()

        recompute_book_rating.delay(book_id)

    async def delete_review(self, book_id: int, review_id: int, current_user: UsersOrm):
        review = await self.db.reviews.get_one_or_none(id=review_id)
        if review is None or review.book_id != book_id:
            raise ReviewNotFoundException
        if review.user_id != current_user.id and current_user.role.name != "ADMIN":
            raise CanDeleteOnlyOwnReviewException

        await self.db.reviews.delete(id=review_id)
        await self.db.commit()

        recompute_book_rating.delay(book_id)
