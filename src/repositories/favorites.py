from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload

from src.models import FavoritesOrm, BooksOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FavoriteDataMapper
from src.schemas.favorites import FavoriteBookOut


class FavoritesRepository(BaseRepository):
    model = FavoritesOrm
    mapper = FavoriteDataMapper
    schema = FavoriteBookOut

    async def get_all(self, user_id: int):
        query = (select(self.model)
                 .filter(self.model.user_id == user_id)
                 .options(
                     selectinload(FavoritesOrm.book)
                     .selectinload(BooksOrm.author)
                )
        )
        result = await self.session.execute(query)
        favorites = result.scalars().all()
        return [self.schema.model_validate(f.book) for f in favorites]
        """
        return [self.mapper.map_to_domain_entity(f) for f in favorites]
        """

    async def add(self, book_id: int, user_id: int):
        add_data_stmt = insert(self.model).values(
            book_id=book_id,
            user_id=user_id
        ).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)