from fastapi import HTTPException
from pydantic import EmailStr, BaseModel
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from src.models import UsersOrm, RolesOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas.users import UserWithHashedPassword, UserUpdateRole


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_users(self, limit, offset):
        query = select(UsersOrm).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(user) for user in result.scalars().all()]

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return UserWithHashedPassword.model_validate(model)

    """
    async def update_user_role(self, user_id: int, payload: UserUpdateRole):
        
        user = await self.session.execute(
            select(UsersOrm)
            .filter_by(user_id=user_id)
        )
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        role = await self.session.execute(
            select(RolesOrm)
            .filter_by(name=payload.role)
        )
        if role is None:
            raise HTTPException(status_code=400, datail="Такой роли не существует")
        
        user.role_id = role.id

        query = await self.session.execute(
            update(UsersOrm)
            .filter_by(user_id=user_id)
            .values()
        )
    """

    async def get_one_orm(self, **filter_by) -> BaseModel | None:
        query = (
            select(self.model)
            .filter_by(**filter_by)
            .options(
                selectinload(self.model.role)
            )
        )
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

