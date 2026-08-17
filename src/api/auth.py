from fastapi import APIRouter, Response, Request
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import (
    EmailAlreadyExistsException,
    EmailAlreadyExistsHTTPException,
    UsernameAlreadyExistsException,
    UsernameAlreadyExistsHTTPException,
    IncorrectCredentialsException,
    IncorrectCredentialsHTTPException,
    UserInactiveException,
    UserInactiveHTTPException,
)
from src.schemas.users import UserRegister, UserLogin
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
        data: UserRegister,
        db: DBDep
):
    try:
        await AuthService(db).register_user(data)
    except EmailAlreadyExistsException:
        raise EmailAlreadyExistsHTTPException
    except UsernameAlreadyExistsException:
        raise UsernameAlreadyExistsHTTPException
    return {"status": "OK"}

@router.post("/login")
async def login_user(
        data: UserLogin,
        response: Response,
        db: DBDep
):
    try:
        access_token = await AuthService(db).login_user(data)
    except IncorrectCredentialsException:
        raise IncorrectCredentialsHTTPException
    except UserInactiveException:
        raise UserInactiveHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}

@router.get("/me", summary="🧑‍💻 Мой профиль")
@cache(expire=300)
async def get_me(
        user_id: UserIdDep,
        db: DBDep
):
    return await AuthService(db).get_one_or_none_user(user_id)

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
