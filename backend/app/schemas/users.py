from pydantic import BaseModel, ConfigDict

# Базовые
class UserBase(BaseModel):
    email: str
    name: str | None = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Чтение из ORM
class UserRead(BaseModel):
    id: int
    email: str
    name: str | None = None
    avatar_url: str | None = None

class PasswordChange(BaseModel):
    old_password: str
    new_password: str
    new_password2: str

    model_config = ConfigDict(from_attributes=True)
