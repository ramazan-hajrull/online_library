"""create analytics materialized views

Revision ID: 731ca3004f24
Revises: cbb42eb63ebd
Create Date: 2026-08-08 16:26:12.119854

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "731ca3004f24"
down_revision: Union[str, Sequence[str], None] = "cbb42eb63ebd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE MATERIALIZED VIEW mv_top_books AS
        SELECT
            b.id AS book_id,
            b.title AS title,
            a.full_name AS author_name,
            b.average_rating AS average_rating,
            b.reviews_count AS reviews_count,
            COALESCE(f.favorites_count, 0) AS favorites_count
        FROM books b
        JOIN authors a ON a.id = b.author_id
        LEFT JOIN (
            SELECT book_id, COUNT(*) AS favorites_count
            FROM favorites
            GROUP BY book_id
        ) f ON f.book_id = b.id
        WITH DATA;
        """
    )
    # REFRESH MATERIALIZED VIEW CONCURRENTLY требует уникальный индекс
    op.execute(
        "CREATE UNIQUE INDEX ix_mv_top_books_book_id ON mv_top_books (book_id);"
    )

    op.execute(
        """
        CREATE MATERIALIZED VIEW mv_author_stats AS
        SELECT
            a.id AS author_id,
            a.full_name AS full_name,
            COUNT(DISTINCT b.id) AS books_count,
            COALESCE(AVG(b.average_rating), 0) AS avg_book_rating,
            COALESCE(SUM(b.reviews_count), 0) AS total_reviews
        FROM authors a
        LEFT JOIN books b ON b.author_id = a.id
        GROUP BY a.id, a.full_name
        WITH DATA;
        """
    )
    op.execute(
        "CREATE UNIQUE INDEX ix_mv_author_stats_author_id ON mv_author_stats (author_id);"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP MATERIALIZED VIEW IF EXISTS mv_author_stats;")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS mv_top_books;")
