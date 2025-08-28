from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database.session import get_db
from app.models.orders import Order, OrderItem
from app.models.users import User
from app.models.chat import ChatRoom
from app.schemas.orders import OrderCreate, OrderRead
from app.core.security import get_current_user
from app.services.orders import create_order_service, checkout_service
from app.services.chat_service import create_chat_for_order

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderRead)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    order = create_order_service(db, current_user.id, order_data)
    create_chat_for_order(db, order.id, client_id=current_user.id)

    return order


@router.post("/checkout")
def checkout(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order_id = payload.get("order_id")
    payment_method = payload.get("payment_method")

    if not order_id or not payment_method:
        raise HTTPException(status_code=400, detail="order_id and payment_method required")

    # выполняем логику оплаты
    result = checkout_service(db, order_id, current_user.id, payment_method)

    # ищем чат, связанный с заказом
    chat = db.query(ChatRoom).filter(ChatRoom.order_id == order_id).first()

    return {
        "order_id": order_id,
        "status": result["status"] if isinstance(result, dict) and "status" in result else "paid",
        "chat_id": chat.id if chat else None
    }


@router.get("/me", response_model=List[OrderRead])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orders = db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.item),
        joinedload(Order.user)
    ).filter(Order.user_id == current_user.id).all()

    for o in orders:
        chat = db.query(ChatRoom).filter(ChatRoom.order_id == o.id).first()
        setattr(o, "chat_id", chat.id if chat else None)

    return orders

@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.item),
        joinedload(Order.user)
    ).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    chat = db.query(ChatRoom).filter(ChatRoom.order_id == order.id).first()
    setattr(order, "chat_id", chat.id if chat else None)

    return order


