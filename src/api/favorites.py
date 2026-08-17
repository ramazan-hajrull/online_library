from fastapi import APIRouter, Depends

from src.api.dependencies import DBDep, get_current_user_id
from src.exceptions import FavoriteNotFoundException, FavoriteNotFoundHTTPException
from src.services.favorites import FavoriteService

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.get("")
async def list_favorites(
        db: DBDep,
        user_id = Depends(get_current_user_id)
):
    return await FavoriteService(db).get_favorite(user_id)

@router.post("/{book_id}")
async def add_favorite(
        book_id: int,
        db: DBDep,
        user_id = Depends(get_current_user_id)
):
    favorite = await FavoriteService(db).add_favorite(book_id, user_id)
    return {"status": "OK", "data": favorite}

@router.delete("/{book_id}")
async def remove_favorite(
        book_id: int,
        db: DBDep,
        user_id = Depends(get_current_user_id)
):
    try:
        await FavoriteService(db).remove_favorite(book_id, user_id)
    except FavoriteNotFoundException:
        raise FavoriteNotFoundHTTPException
    return {"status": "OK"}
