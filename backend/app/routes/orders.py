from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.core.settings import stripe_api_key
from app.database.session import get_db
from app.models.orders import Order, OrderItem
from app.models.users import User
from app.schemas.orders import OrderCreate, OrderRead
from app.core.security import get_current_user
from app.models.items import Item
import stripe

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderRead)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not order_data.items:
        raise HTTPException(status_code=400, detail="No items provided")

    total_price = 0
    order = Order(user_id=current_user.id, status="pending", total_price=0)
    db.add(order)
    db.flush()

    for item_data in order_data.items:
        db_item = db.query(Item).filter(Item.id == item_data.item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail=f"Item {item_data.item_id} not found")

        db.add(OrderItem(
            order_id=order.id,
            item_id=item_data.item_id,
            quantity=item_data.quantity,
            price=item_data.price
        ))

        total_price += item_data.price * item_data.quantity

    order.total_price = total_price
    db.commit()

    # Подгрузка связанных данных для ответа
    order = db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.item),
        joinedload(Order.user)
    ).filter(Order.id == order.id).first()

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

    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if payment_method == "stripe":
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                mode="payment",
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": f"Order #{order.id}"
                            },
                            "unit_amount": int(order.total_price * 100),
                        },
                        "quantity": 1,
                    }
                ],
                success_url="http://localhost:5173/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://localhost:5173/cancel",
                metadata={"order_id": order.id}
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        return {"checkout_url": session.url}

    raise HTTPException(status_code=400, detail="Unsupported payment method")

@router.get("/me", response_model=List[OrderRead])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.item),
        joinedload(Order.user)
    ).filter(Order.user_id == current_user.id).all()

@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.item),
        joinedload(Order.user)
    ).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get('/', response_model=list[OrderRead])
def get_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Order).filter(Order.user_id == current_user.id).all()