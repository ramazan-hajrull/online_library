from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    full_name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    user_id: int


class AuthorUpdate(BaseModel):
    full_name: str | None = None
    bio: str | None = None


class Author(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)