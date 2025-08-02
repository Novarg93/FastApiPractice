from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from schemas.order import OrderRead      # Импорт для истории заказов
from schemas.items import ItemRead        # Импорт для избранного/корзины

# Основные поля пользователя
class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        from_attributes = True

# Схема для регистрации пользователя
class UserCreate(UserBase):
    password: str

# Схема для ответа с ID и признаком администратора
class UserResponse(UserBase):
    id: int
    is_admin: bool = False

    class Config:
        from_attributes = True

# Схема для смены пароля
class UserChangePassword(BaseModel):
    old_password: str
    new_password: str

# Схема для подтверждения email через код
class EmailVerificationRequest(BaseModel):
    email: EmailStr

class EmailVerificationConfirm(BaseModel):
    email: EmailStr
    code: str

# Избранное (Favorites) — список товаров
class FavoritesList(BaseModel):
    items: List[ItemRead]

    class Config:
        from_attributes = True

# Корзина пользователя
class CartItemRead(BaseModel):
    item: ItemRead
    quantity: int

    class Config:
        from_attributes = True

class CartRead(BaseModel):
    items: List[CartItemRead]
    total_price: float
    count: int

    class Config:
        from_attributes = True

# История заказов пользователя
class UserProfile(UserResponse):
    orders: List[OrderRead] = []
    favorites: List[ItemRead] = []
    cart: Optional[CartRead] = None

    class Config:
        from_attributes = True


#FAVORITE
class FavoriteAdd(BaseModel):
    item_id: int

class FavoriteRemove(BaseModel):
    item_id: int

class FavoriteRead(BaseModel):
    item: ItemRead

    class Config:
        from_attributes = True

class FavoritesList(BaseModel):
    items: List[ItemRead]

    class Config:
        from_attributes = True

