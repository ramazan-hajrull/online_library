import asyncio
from datetime import datetime, timedelta, UTC
import logging

import redis as sync_redis
from sqlalchemy import func, select, text

from src.config import settings
from src.database import async_session_maker_null_pool, engine_null_pool
from src.models import ReviewsOrm
from src.tasks import celery_app
from src.tasks.celery_app import celery_instance
from src.tasks.report_service import generate_library_stats_excel, generate_library_stats_pdf
from src.utils.db_manager import DBManager


logger = logging.getLogger(__name__)


async def notify_author_helper(review_id: int) -> None:
    async with DBManager(
        session_factory=async_session_maker_null_pool
    ) as db:
        review = await db.reviews.get_one_or_none(id=review_id)
        if review is None:
            logger.warning("notify_author: review %s not found", review_id)
            return
        book = await db.books.get_book_with_author(id=review.book_id)
        if book is None or book.author is None:
            logger.warning("notify_author: book/author not found for review %s", review_id)
            return

        author_email = book.author.user.email if book.author.user else None
        logger.info(
            "Notifying author %s about new review (rating=%s) on book '%s' (email=%s)",
            book.author.full_name, review.rating, book.title, author_email
        )

@celery_instance.task(name="notify_author")
def notify_author(review_id: int):
    asyncio.run(
        notify_author_helper(review_id)
    )


async def recompute_book_rating_helper(book_id: int) -> None:
    async with DBManager(
        session_factory=async_session_maker_null_pool
    ) as db:
        avg_rating, count = await db.reviews.get_book_rating_stats(book_id)
        book = await db.books.get_one_or_none(id=book_id)
        if book is None:
            return

        book.average_rating = round(float(avg_rating or 0), 2)
        book.reviews_count = int(count or 0)
        await db.commit()

    _clear_cache_pattern("fastapi-cache:books:*")

@celery_instance.task(name="recompute_book_rating")
def recompute_book_rating(book_id: int):
    asyncio.run(
        recompute_book_rating_helper(book_id)
    )


def _clear_cache_pattern(pattern: str) -> None:
    """Синхронный сброс ключей fastapi-cache2 по паттерну -- используется из
    Celery worker'а, у которого нет доступа к event loop'у FastAPI."""
    client = sync_redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    try:
        cursor = 0
        while True:
            cursor, keys = client.scan(cursor=cursor, match=pattern, count=200)
            if keys:
                client.delete(*keys)
            if cursor == 0:
                break
    finally:
        client.close()

async def _refresh_materialized_views_helper() -> None:
    async with engine_null_pool.connect() as conn:
        await conn.execute(text("REFRESH MATERIALIZED VIEW CONCURRENTLY mv_top_books"))
        await conn.execute(text("REFRESH MATERIALIZED VIEW CONCURRENTLY mv_author_stats"))
        await conn.commit()


@celery_instance.task(name="refresh_materialized_views")
def refresh_materialized_views():
    asyncio.run(_refresh_materialized_views_helper())
    logger.info("Materialized views refreshed")


async def _generate_admin_report_helper(days: int = 30, fmt: str = "pdf") -> str:
    async with DBManager(
        session_factory=async_session_maker_null_pool
    ) as db:
        since = (datetime.now(UTC) - timedelta(days=days)).replace(tzinfo=None)

        new_books = await db.books.count_books(since=since)
        new_reviews = await db.reviews.count_reviews(since=since)
        active_users = await db.reviews.count_active_users(since=since)
        top_books_rows = await db.books.top_books(since=since)

        top_books = [
            {"title": t, "average_rating": r or 0.0, "reviews_count": c}
            for t, r, c in top_books_rows
        ]

        stats = {
            "generated_at": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S"),
            "new_books": new_books,
            "new_reviews": new_reviews,
            "active_users": active_users,
            "top_books": top_books
        }

        if fmt == "xlsx":
            return generate_library_stats_excel(stats)
        return generate_library_stats_pdf(stats)


@celery_instance.task(name="generate_admin_report")
def generate_admin_report(days: int = 30, fmt: str = "pdf") -> str:
    return asyncio.run(_generate_admin_report_helper(days, fmt))