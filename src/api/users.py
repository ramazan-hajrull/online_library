from fastapi import APIRouter, Depends

from src.api.dependencies import DBDep, require_admin, PaginationDep
from src.schemas.users import UserUpdateRole, UserUpdateBlock
from src.services.users import UsersService

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("", dependencies=[Depends(require_admin)])
async def list_users(
        pagination: PaginationDep,
        db: DBDep
):
    return await UsersService(db).get_users(pagination)

@router.patch("/{user_id}/role", dependencies=[Depends(require_admin)])
async def update_user_role(user_id: int, payload: UserUpdateRole, db: DBDep):
    await UsersService(db).update_role(user_id, payload)
    return {"status": "OK"}


@router.patch("/{user_id}/block", dependencies=[Depends(require_admin)])
async def toggle_block_user(user_id: int, payload: UserUpdateBlock, db: DBDep):
    await UsersService(db).update_is_blocked(user_id, payload)
    return {"status": "OK"}