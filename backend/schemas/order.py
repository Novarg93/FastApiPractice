from pydantic import BaseModel
from typing import Optional, List
import enum
from schemas.items import ItemRead  # Импорт для вложенных товаров

class OrderStatus(str, enum.Enum):
    pending = "Pending"
    delivering = "Delivering"
    completed = "Completed"

class OrderItem(BaseModel):
    item: ItemRead
    quantity: int

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    status: OrderStatus
    total_price: float
    coupon_code: Optional[str] = None

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    items: List[OrderItem]
    coupon_code: Optional[str] = None

    class Config:
        from_attributes = True

class OrderRead(OrderBase):
    id: int
    items: List[OrderItem]
    created_at: Optional[str]

    class Config:
        from_attributes = True

class OrderConfirm(BaseModel):
    order_id: int

class OrdersHistory(BaseModel):
    orders: List[OrderRead]

    class Config:
        from_attributes = True
