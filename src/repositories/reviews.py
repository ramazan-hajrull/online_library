from datetime import datetime

from sqlalchemy import select, func

from src.models import ReviewsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import ReviewDataMapper


class ReviewRepository(BaseRepository):
    model = ReviewsOrm
    mapper = ReviewDataMapper

    async def count_reviews(self, since: datetime):
        query = (
            select(func.count(ReviewsOrm.id))
            .where(ReviewsOrm.created_at >= since)
        )
        result = await self.session.execute(query)
        return result.scalars().one()

    async def get_book_rating_stats(self, book_id: int):
        query = select(
            func.avg(ReviewsOrm.rating), func.count(ReviewsOrm.id)
        ).where(ReviewsOrm.book_id == book_id)
        result = await self.session.execute(query)
        return result.one()

    async def count_active_users(self, since: datetime):
        query = (
            select(func.count(func.distinct(ReviewsOrm.user_id)))
            .where(ReviewsOrm.created_at >= since)
        )
        result = await self.session.execute(query)
        return result.scalars().one() or 0