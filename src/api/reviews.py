from fastapi import APIRouter, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, get_current_user, UserIdDep
from src.exceptions import (
    ReviewAlreadyExistsException,
    ReviewAlreadyExistsHTTPException,
    ReviewNotFoundException,
    ReviewNotFoundHTTPException,
    CanEditOnlyOwnReviewException,
    CanEditOnlyOwnReviewHTTPException,
    CanDeleteOnlyOwnReviewException,
    CanDeleteOnlyOwnReviewHTTPException,
)
from src.schemas.reviews import ReviewAddRequest, ReviewUpdate
from src.services.reviews import ReviewService

router = APIRouter(prefix="/api/books/{book_id}/reviews", tags=["reviews"])


@router.get("")
@cache(expire=10, namespace="books")
async def list_reviews(book_id: int, db: DBDep):
    return await ReviewService(db).list_reviews(book_id)

@router.post("")
async def create_review(
        book_id: int,
        payload: ReviewAddRequest,
        db: DBDep,
        user_id: UserIdDep):
    try:
        review = await ReviewService(db).create_review(book_id, payload, user_id)
    except ReviewAlreadyExistsException:
        raise ReviewAlreadyExistsHTTPException
    await FastAPICache.clear(namespace="books")
    return {"status": "OK", "data": review}

@router.put("/{review_id}")
async def update_review(
        book_id: int,
        review_id: int,
        payload: ReviewUpdate,
        db: DBDep,
        current_user = Depends(get_current_user)
):
    try:
        await ReviewService(db).update_review(book_id, payload, current_user, review_id)
    except ReviewNotFoundException:
        raise ReviewNotFoundHTTPException
    except CanEditOnlyOwnReviewException:
        raise CanEditOnlyOwnReviewHTTPException
    await FastAPICache.clear(namespace="books")
    return {"status": "OK"}

@router.delete("/{review_id}")
async def delete_review(
        book_id: int,
        review_id: int,
        db: DBDep,
        current_user = Depends(get_current_user)
):
    try:
        await ReviewService(db).delete_review(book_id, review_id, current_user)
    except ReviewNotFoundException:
        raise ReviewNotFoundHTTPException
    except CanDeleteOnlyOwnReviewException:
        raise CanDeleteOnlyOwnReviewHTTPException
    await FastAPICache.clear(namespace="books")
    return {"status": "OK"}
