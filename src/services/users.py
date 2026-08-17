from fastapi_cache import FastAPICache

from src.api.dependencies import PaginationParams
from src.schemas.authors import AuthorCreate
from src.schemas.users import UserUpdateRole, UserUpdateBlock
from src.services.base import BaseService


class UsersService(BaseService):
    async def get_users(self, pagination: PaginationParams):
        per_page = pagination.per_page or 5
        return await self.db.users.get_users(
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )

    async def update_role(self, user_id: int, payload: UserUpdateRole):
        await self.db.users.edit(data=payload, exclude_unset=True, id=user_id)
        role = await self.db.roles.get_one_or_none(id=payload.role_id)
        if role.name == "AUTHOR":
            existing_author = await self.db.authors.get_one_or_none(user_id=user_id)
            if existing_author is None:
                user = await self.db.users.get_one_or_none(id=user_id)
                await self.db.authors.add(
                    AuthorCreate(user_id=user_id, full_name=user.username)
                )
            await FastAPICache.clear(namespace="authors")
        await self.db.commit()

    async def update_is_blocked(self, user_id: int, payload: UserUpdateBlock):
        await self.db.users.edit(data=payload, exclude_unset=True, id=user_id)
        await self.db.commit()