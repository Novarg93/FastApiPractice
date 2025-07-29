from pydantic import BaseModel, EmailStr
from typing import Optional, List

# Основные поля пользователя
class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_admin: bool

# Адреса пользователя
class Address(BaseModel):
    user_id: int
    street: str
    city: str
    postal_code: str
    country: str

# Лист пожеланий
class Wishlist(BaseModel):
    user_id: int
    item_ids: List[int]

# Роли и права
class Role(BaseModel):
    name: str
    permissions: List[str]

class Permission(BaseModel):
    name: str
    description: Optional[str]
