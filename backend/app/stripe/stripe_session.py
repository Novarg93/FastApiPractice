from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import stripe

from app.database.session import get_db
from app.models.orders import Order
from app.models.users import User
from app.core.security import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])

class StripeCreateResp(BaseModel):
    checkout_url: str
    session_id: str

@router.post("/stripe/create", response_model=StripeCreateResp)
def stripe_create(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. Проверяем, что заказ существует и принадлежит текущему юзеру
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    try:
        # 2. Создаём Checkout-сессию
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": f"Order #{order.id}",
                        },
                        "unit_amount": int(order.total_price * 100),  # цена в центах
                    },
                    "quantity": 1,
                }
            ],
            success_url="http://localhost:8000/orders/stripe/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:8000/orders/stripe/cancel",
            metadata={"order_id": str(order.id)},
        )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Stripe error: {e}")

    # 3. Возвращаем ссылку для фронта
    return {
        "checkout_url": session.url,
        "session_id": session.id,
    }
