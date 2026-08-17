import enum

from sqlalchemy import ForeignKey, String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

"""
class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    AUTHOR = "author"
    USER = "user"
"""

class RolesOrm(Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(unique=True)

