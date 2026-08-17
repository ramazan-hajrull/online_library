from datetime import datetime

from sqlalchemy import select, asc, desc, func, update
from sqlalchemy.orm import selectinload


from src.models import BooksOrm, FavoritesOrm, AuthorsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookDataMapper
from src.schemas.books import BookFilterParams


class BooksRepository(BaseRepository):
    model = BooksOrm
    mapper = BookDataMapper

    async def get_filtered(self, filters: BookFilterParams):
        query = select(BooksOrm)
        if filters.author_id is not None:
            query = query.filter(BooksOrm.author_id == filters.author_id)
        if filters.min_rating is not None:
            query = query.filter(BooksOrm.average_rating >= filters.min_raiting)
        if filters.search:
            like = f"%{filters.search}%"
            query = query.filter(BooksOrm.title.ilike(like))

        sort_column = getattr(BooksOrm, filters.sort_by)
        query = query.order_by(asc(sort_column) if filters.order == "asc" else desc(sort_column))

        offset = (filters.page - 1) * filters.page_size
        query = query.offset(offset).limit(filters.page_size)
        result = await self.session.execute(query)
        books = result.scalars().all()

        return [self.mapper.map_to_domain_entity(b) for b in books]


    async def get_book_with_author(self, book_id: int):
        query = (
            select(BooksOrm)
            .options(
                selectinload(BooksOrm.author)
                .selectinload(AuthorsOrm.user)
            )
            .filter(BooksOrm.id == book_id)
        )
        result = await self.session.execute(query)
        return result.scalars().one_or_none()


    async def count_books(self, since: datetime):
        query = (
            select(func.count(BooksOrm.id))
            .where(BooksOrm.created_at >= since)
        )
        result = await self.session.execute(query)
        return result.scalars().one()

    async def top_books(self, since: datetime | None = None, limit: int = 10):
        query = select(
            BooksOrm.title,
            BooksOrm.average_rating,
            BooksOrm.reviews_count
        )
        if since is not None:
            query = query.where(BooksOrm.created_at >= since)
        query = query.order_by(
            BooksOrm.average_rating.desc(),
            BooksOrm.reviews_count.desc()
        ).limit(limit)
        result = await self.session.execute(query)
        return result.all()

    async def set_cover_path(self, book_id: int, cover_path: str):
        stmt = update(BooksOrm).filter_by(id=book_id).values(cover_path=cover_path)
        await self.session.execute(stmt)

    async def set_file_path(self, book_id: int, file_path: str):
        stmt = update(BooksOrm).filter_by(id=book_id).values(file_path=file_path)
        await self.session.execute(stmt)

    async def set_rating(self, book_id: int, average_rating: float, reviews_count: int):
        stmt = (
            update(BooksOrm)
            .filter_by(id=book_id)
            .values(average_rating=average_rating, reviews_count=reviews_count)
        )
        await self.session.execute(stmt)

