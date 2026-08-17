from src.exceptions import ObjectNotFoundException, AuthorNotFoundException
from src.schemas.authors import AuthorCreate, AuthorUpdate
from src.schemas.users import UserUpdateRole
from src.services.base import BaseService


class AuthorService(BaseService):
    async def create_author(self, data: AuthorCreate):
        author = await self.db.authors.add(data)
        role = await self.db.roles.get_one_or_none(name="AUTHOR")
        await self.db.users.edit(
            UserUpdateRole(role_id=role.id),
            exclude_unset=True,
            id=data.user_id
        )
        await self.db.commit()
        return author

    async def get_authors(self):
        return await self.db.authors.get_all()

    async def get_author(self, author_id: int):
        try:
            return await self.db.authors.get_one(id=author_id)
        except ObjectNotFoundException:
            raise AuthorNotFoundException

    async def update_author(self, data: AuthorUpdate, author_id: int):
        try:
            await self.db.authors.get_one(id=author_id)
        except ObjectNotFoundException:
            raise AuthorNotFoundException
        await self.db.authors.edit(data=data, exclude_unset=True, id=author_id)
        await self.db.commit()

    async def delete_author(self, author_id: int):
        await self.db.authors.delete(id=author_id)
        await self.db.commit()
