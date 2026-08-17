from src.repositories.authors import AuthorsRepository
from src.repositories.books import BooksRepository
from src.repositories.favorites import FavoritesRepository
from src.repositories.reviews import ReviewRepository
from src.repositories.roles import RolesRepository
from src.repositories.users import UsersRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.authors = AuthorsRepository(self.session)
        self.users = UsersRepository(self.session)
        self.roles = RolesRepository(self.session)
        self.books = BooksRepository(self.session)
        self.reviews = ReviewRepository(self.session)
        self.favorites = FavoritesRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
