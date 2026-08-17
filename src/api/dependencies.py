from typing import Annotated, Literal

from fastapi import Request, Depends, Query
from pydantic import BaseModel

from src.database import async_session_maker
from src.exceptions import (
    IncorrectTokenException,
    IncorrectTokenHTTPException,
    NoAccessTokenHTTPException,
    UserNotFoundHTTPException,
    UserBlockedHTTPException,
    InsufficientPermissionsHTTPException,
)
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30)]

PaginationDep = Annotated[PaginationParams, Depends()]

def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise NoAccessTokenHTTPException

    return token

def get_current_user_id(token: str = Depends(get_token)):
    try:
        data = AuthService().decode_token(token)
    except IncorrectTokenException:
        raise IncorrectTokenHTTPException
    return data["user_id"]

UserIdDep = Annotated[int, Depends(get_current_user_id)]

async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]

async def get_current_user(db: DBDep, user_id: UserIdDep):
    user = await db.users.get_one_orm(id=user_id)
    if user is None:
        raise UserNotFoundHTTPException
    if user.is_blocked:
        raise UserBlockedHTTPException
    return user

def require_roles(*allowed_roles: str):
    async def cheсker(current_user = Depends(get_current_user)):
        if current_user.role.name not in allowed_roles:
            raise InsufficientPermissionsHTTPException
        return current_user
    return cheсker

require_admin = require_roles("ADMIN")
require_author = require_roles("ADMIN", "AUTHOR")
