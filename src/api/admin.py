from fastapi import Depends, APIRouter
from sqlalchemy import text
from fastapi.responses import FileResponse

from src.api.dependencies import require_admin, DBDep
from src.tasks.celery_app import celery_instance
from src.tasks.tasks import generate_admin_report

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])


@router.post("/reports/{fmt}")
def request_report(fmt: str, days: int = 30):
    task = generate_admin_report.delay(days=days, fmt=fmt)
    return {"task_id": task.id, "status": "queued"}


@router.get("/reports/status/{task_id}")
def report_status(task_id: str):
    result = celery_instance.AsyncResult(task_id)
    payload = {"task_id": task_id, "state": result.state}
    if result.state == "SUCCESS":
        payload["file_path"] = result.result
    elif result.state == "FAILURE":
        payload["error"] = str(result.result)
    return payload


@router.get("/reports/download")
def download_report(file_path: str):
    return FileResponse(file_path, filename=file_path.split("/")[-1])


@router.get("/analytics/top-books")
async def top_books(db: DBDep, limit: int = 20):
    rows = (await db.session.execute(
        text(
            "SELECT book_id, title, author_name, average_rating, reviews_count, favorites_count "
            "FROM mv_top_books ORDER BY average_rating DESC, reviews_count DESC LIMIT :limit"
        ),
        {"limit": limit},
    )).mappings().all()
    return [dict(r) for r in rows]


@router.get("/analytics/author-stats")
async def author_stats(db: DBDep, limit: int = 20):
    rows = (await db.session.execute(
        text(
            "SELECT author_id, full_name, books_count, avg_book_rating, total_reviews "
            "FROM mv_author_stats ORDER BY avg_book_rating DESC LIMIT :limit"
        ),
        {"limit": limit},
    )).mappings().all()
    return [dict(r) for r in rows]