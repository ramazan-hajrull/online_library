from fastapi import APIRouter, Depends, UploadFile
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from src.api.dependencies import require_admin, DBDep, require_author, get_current_user
from src.exceptions import (
    AuthorNotFoundException,
    AuthorNotFoundHTTPException,
    BookNotFoundException,
    BookNotFoundHTTPException,
    OnlyAdminOrAuthorException,
    OnlyAdminOrAuthorHTTPException,
    AuthorCanOnlyAddOwnBooksException,
    AuthorCanOnlyAddOwnBooksHTTPException,
    CanEditOnlyOwnBooksException,
    CanEditOnlyOwnBooksHTTPException,
)
from src.schemas.books import BookCreate, BookUpdate, BookFilterParams
from src.services.books import BooksService

router = APIRouter(prefix="/books", tags=["books"])


@router.get("")
@cache(expire=60, namespace="books")
async def get_books(db: DBDep, filters: BookFilterParams = Depends()):
    return await BooksService(db).get_books(filters)

@router.get("/{book_id}")
@cache(expire=60, namespace="books")
async def get_book(book_id: int, db: DBDep):
    return await BooksService(db).get_book(book_id)

@router.post("")
async def create_book(
        payload: BookCreate,
        db: DBDep,
        current_user = Depends(get_current_user)
):
    try:
        book = await BooksService(db).create_book(payload, current_user)
    except OnlyAdminOrAuthorException:
        raise OnlyAdminOrAuthorHTTPException
    except AuthorNotFoundException:
        raise AuthorNotFoundHTTPException
    except AuthorCanOnlyAddOwnBooksException:
        raise AuthorCanOnlyAddOwnBooksHTTPException
    await FastAPICache.clear(namespace="books")
    return {"status": "OK", "data": book}

@router.put("/{book_id}")
async def update_book(
        book_id: int,
        payload: BookUpdate,
        db: DBDep,
        current_user = Depends(get_current_user)
):
    try:
        await BooksService(db).update_book(book_id, payload, current_user)
    except BookNotFoundException:
        raise BookNotFoundHTTPException
    except CanEditOnlyOwnBooksException:
        raise CanEditOnlyOwnBooksHTTPException
    await FastAPICache.clear(namespace="books")
    return {"status": "OK"}

@router.delete("/{book_id}")
async def delete_book(
        book_id: int,
        db: DBDep,
        current_user = Depends(get_current_user)
):
    try:
        await BooksService(db).delete_book(book_id, current_user)
    except BookNotFoundException:
        raise BookNotFoundHTTPException
    except CanEditOnlyOwnBooksException:
        raise CanEditOnlyOwnBooksHTTPException
    await FastAPICache.clear(namespace="books")
    return {"status": "OK"}

@router.post("/{book_id}/cover")
async def upload_book_cover(
        book_id: int,
        file: UploadFile,
        db: DBDep,
        current_user = Depends(get_current_user)
):
    try:
        book = await BooksService(db).upload_cover(book_id, file, current_user)
    except BookNotFoundException:
        raise BookNotFoundHTTPException
    except CanEditOnlyOwnBooksException:
        raise CanEditOnlyOwnBooksHTTPException
    await FastAPICache.clear(namespace="books")
    return {"status": "OK", "data": book}

@router.post("/{book_id}/file")
async def upload_book_file(
        book_id: int,
        file: UploadFile,
        db: DBDep,
        current_user = Depends(get_current_user)
):
    try:
        book = await BooksService(db).upload_file(book_id, file, current_user)
    except BookNotFoundException:
        raise BookNotFoundHTTPException
    except CanEditOnlyOwnBooksException:
        raise CanEditOnlyOwnBooksHTTPException
    await FastAPICache.clear(namespace="books")
    return {"status": "OK", "data": book}
