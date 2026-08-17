from src.exceptions import FavoriteNotFoundException
from src.services.base import BaseService


class FavoriteService(BaseService):
    async def get_favorite(self, user_id: int):
        return await self.db.favorites.get_all(user_id=user_id)

    async def add_favorite(self, book_id: int, user_id: int):
        existing = await self.db.favorites.get_one_or_none(book_id=book_id, user_id=user_id)
        if existing:
            return existing

        favorite = await self.db.favorites.add(book_id=book_id, user_id=user_id)
        await self.db.commit()
        return favorite

    async def remove_favorite(self, book_id: int, user_id: int):
        favorite = await self.db.favorites.get_one_or_none(book_id=book_id, user_id=user_id)
        if not favorite:
            raise FavoriteNotFoundException
        await self.db.favorites.delete(book_id=book_id, user_id=user_id)
        await self.db.commit()
