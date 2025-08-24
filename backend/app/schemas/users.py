from pydantic import BaseModel, ConfigDict, constr, EmailStr, field_validator
from app.models.users import UserRole


# Базовые
class UserBase(BaseModel):
    email: EmailStr
    name: constr(min_length=4, max_length=25) | None = None

class UserCreate(UserBase):
    password: constr(min_length=4, max_length=50) | None = None
    role: UserRole = UserRole.USER

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least 1 digits")
        if not any(c.isalpha() for c in v):
            raise ValueError("Password must contain at least 1 letter")
        return v

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserRead(BaseModel):
    id: int
    email: str
    name: str | None = None
    avatar_url: str | None = None
    role: UserRole

class UserUpdate(BaseModel):
    name: constr(min_length=1, max_length=20)

class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

    model_config = ConfigDict(from_attributes=True)
