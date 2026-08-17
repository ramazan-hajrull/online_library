from pydantic import EmailStr, BaseModel, ConfigDict


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(UserLogin):
    username: str

class UserAdd(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    role_id: int

class UserUpdateRole(BaseModel):
    role_id: int

class UserUpdateBlock(BaseModel):
    is_blocked: bool

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    role_id: int
    is_blocked: bool

    model_config = ConfigDict(from_attributes=True)

class UserWithHashedPassword(User):
    hashed_password: str

