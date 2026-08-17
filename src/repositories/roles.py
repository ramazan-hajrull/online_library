from sqlalchemy import select

from src.models import RolesOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoleDataMapper


class RolesRepository(BaseRepository):
    model = RolesOrm
    mapper = RoleDataMapper

    async def get_default_role_id(self):
        query = select(RolesOrm.id).filter_by(name="USER")
        result = await self.session.execute(query)
        return result.scalars().one()