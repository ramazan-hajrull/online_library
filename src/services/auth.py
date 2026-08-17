from datetime import datetime, timedelta, timezone

import jwt
from sqlalchemy import select
from passlib.context import CryptContext

from src.config import settings
from src.exceptions import (
    ObjectAlreadyExistsException,
    EmailAlreadyExistsException,
    UsernameAlreadyExistsException,
    IncorrectCredentialsException,
    UserInactiveException,
    IncorrectTokenException,
)
from src.models import RolesOrm, UsersOrm
from src.schemas.users import UserAdd, UserRegister, UserLogin
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.PyJWTError:
            raise IncorrectTokenException

    async def register_user(self, data: UserRegister):
        if await self.db.users.get_one_or_none(email=data.email):
            raise EmailAlreadyExistsException
        if await self.db.users.get_one_or_none(username=data.username):
            raise UsernameAlreadyExistsException
        hashed_password = self.hash_password(data.password)
        role_id = await self.db.roles.get_default_role_id()
        new_user_data = UserAdd(username=data.username,
                                email=data.email,
                                hashed_password=hashed_password,
                                role_id=role_id
                                )
        try:
            await self.db.users.add(new_user_data)
        except ObjectAlreadyExistsException as ex:
            raise EmailAlreadyExistsException from ex
        await self.db.commit()

    async def login_user(self, data: UserLogin):
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if user is None or not self.verify_password(data.password, user.hashed_password):
            raise IncorrectCredentialsException
        if user.is_blocked:
            raise UserInactiveException
        access_token = self.create_access_token({"user_id": user.id})
        return access_token

    async def get_one_or_none_user(self, user_id: int):
        return await self.db.users.get_one_or_none(id=user_id)
