from fastapi import APIRouter, Depends
from fastapi_cache import FastAPICache

from fastapi_cache.decorator import cache

from src.api.dependencies import require_admin, DBDep, require_author
from src.exceptions import AuthorNotFoundException, AuthorNotFoundHTTPException
from src.schemas.authors import AuthorCreate, AuthorUpdate
from src.services.authors import AuthorService

router = APIRouter(prefix="/api/authors", tags=["authors"])


@router.get("")
@cache(expire=3600, namespace="authors")
async def get_authors(db: DBDep):
    return await AuthorService(db).get_authors()

@router.post("", dependencies=[Depends(require_admin)])
async def create_author(payload: AuthorCreate, db: DBDep):
    author = await AuthorService(db).create_author(payload)
    await FastAPICache.clear(namespace="authors")
    return {"status": "OK", "data": author}

@router.get("/{author_id}")
@cache(expire=600, namespace="authors")
async def get_author(author_id: int, db: DBDep):
    try:
        return await AuthorService(db).get_author(author_id)
    except AuthorNotFoundException:
        raise AuthorNotFoundHTTPException

@router.put("/{author_id}", dependencies=[Depends(require_author)])
async def update_author(author_id: int, author_data: AuthorUpdate, db: DBDep):
    try:
        await AuthorService(db).update_author(author_data, author_id)
    except AuthorNotFoundException:
        raise AuthorNotFoundHTTPException
    await FastAPICache.clear(namespace="authors")
    return {"status": "OK"}

@router.delete("/{author_id}", dependencies=[Depends(require_admin)])
async def delete_author(author_id: int, db: DBDep):
    await AuthorService(db).delete_author(author_id)
    await FastAPICache.clear(namespace="authors")
    return {"status": "OK"}
