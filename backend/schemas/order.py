from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CartItem(BaseModel):
    item_id: int
    quantity: int

class OrderBase(BaseModel):
    user_id: int
    total_price: float
    status: str

class OrderCreate(OrderBase):
    items: List[CartItem]

class OrderResponse(OrderBase):
    order_id: str
    created_at: datetime
    items: List[CartItem]

class OrderItem(BaseModel):
    order_id: str
    item_id: int
    quantity: int
    price_at_purchase: float

class Payment(BaseModel):
    order_id: str
    amount: float
    currency: str
    status: str

class Shipment(BaseModel):
    order_id: str
    method: str
    tracking_number: Optional[str] = None
    status: str

class Discount(BaseModel):
    code: str
    percent: Optional[float] = None
    amount: Optional[float] = None
    valid_until: datetime
