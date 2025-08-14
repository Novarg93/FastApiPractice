from pydantic import BaseModel, ConfigDict, constr


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

class UserUpdate(BaseModel):
    name: constr(min_length=1, max_length=20)


class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

    model_config = ConfigDict(from_attributes=True)
