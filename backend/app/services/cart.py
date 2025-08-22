from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.database.session import get_db
from app.services.currency_service import calculate_price

router = APIRouter(prefix="/cart", tags=["cart"])

class OptionInput(BaseModel):
    name: str
    value: str

class PriceRequest(BaseModel):
    product_id: int
    quantity: int
    selected_options: List[OptionInput]

@router.post("/price")
def post_price(request: PriceRequest, db: Session = Depends(get_db)):
    try:
        result = calculate_price(
            db,
            request.product_id,
            request.quantity,
            [opt.model_dump() for opt in request.selected_options]
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))