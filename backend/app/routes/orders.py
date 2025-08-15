from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.settings import STRIPE_API_KEY
from app.database.session import SessionLocal
from app.models.orders import Order, OrderItem
from app.models.users import User
from app.schemas.orders import OrderCreate, OrderRead
from app.core.security import get_current_user
from app.models.items import Item
import stripe

router = APIRouter(prefix="/orders", tags=["orders"])
stripe.api_key = STRIPE_API_KEY

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=[OrderRead])
def create_order(order_data: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not order_data.items:
        raise HTTPException(status_code=404, detail="No items")

    new_order = Order(user_id=current_user.id, status="Pending")
    db.add(new_order)
    db.flush()

    for item_data in order_data.items:
        db_item = db.query(Item).filter(Item.id == item_data.id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")

        order_item = OrderItem(
            order_id=new_order.id,
            item_id=db_item.id,
            quantity=item_data.quantity,
            price=item_data.price,
        )
        db.add(order_item)

    db.commit()
    db.refresh(new_order)
    return new_order

@router.post("/checkout")
def checkout(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total_price = sum(item.price * item.quantity for item in order_data.items)

    # Создаём заказ в БД
    order = Order(user_id=current_user.id, total_price=total_price)
    db.add(order)
    db.flush()

    for item in order_data.items:
        db.add(OrderItem(
            order_id=order.id,
            item_id=item.item_id,
            quantity=item.quantity,
            price=item.price
        ))

    db.commit()

    # Stripe Checkout Session
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
                        "unit_amount": int(total_price * 100),
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

@router.get("/me/orders", response_model=List[OrderRead])
def get_my_orders(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
        return db.query(Order).filter(Order.user_id == current_user.id).all()

@router.get("/orders/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get('/', response_model=list[OrderRead])
def get_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Order).filter(Order.user_id == current_user.id).all()