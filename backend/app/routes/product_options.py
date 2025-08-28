from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.options import Option, OptionChoice, ProductOption
from app.schemas.options import (
    OptionSchema, OptionCreate, OptionUpdate,
    OptionChoiceSchema, OptionChoiceCreate, OptionChoiceUpdate,
    ProductOptionCreate
)
from app.models.users import User, UserRole
from app.core.security import get_current_user

router = APIRouter(prefix="/product-options", tags=["product-options"])

# Создать опцию
@router.post("/options", response_model=OptionSchema)
def create_option(
    data: OptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPPORT]:
        raise HTTPException(status_code=403, detail="Not authorized")

    option = Option(**data.dict())
    db.add(option)
    db.commit()
    db.refresh(option)
    return option


# Обновить опцию
@router.patch("/options/{option_id}", response_model=OptionSchema)
def update_option(
    option_id: int,
    data: OptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPPORT]:
        raise HTTPException(status_code=403, detail="Not authorized")

    option = db.query(Option).filter(Option.id == option_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="Option not found")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(option, field, value)

    db.commit()
    db.refresh(option)
    return option


# Создать значение опции
@router.post("/options/{option_id}/choices", response_model=OptionChoiceSchema)
def create_option_choice(
    option_id: int,
    data: OptionChoiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPPORT]:
        raise HTTPException(status_code=403, detail="Not authorized")

    choice = OptionChoice(option_id=option_id, **data.dict())
    db.add(choice)
    db.commit()
    db.refresh(choice)
    return choice


# Обновить значение опции
@router.patch("/choices/{choice_id}", response_model=OptionChoiceSchema)
def update_option_choice(
    choice_id: int,
    data: OptionChoiceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPPORT]:
        raise HTTPException(status_code=403, detail="Not authorized")

    choice = db.query(OptionChoice).filter(OptionChoice.id == choice_id).first()
    if not choice:
        raise HTTPException(status_code=404, detail="Choice not found")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(choice, field, value)

    db.commit()
    db.refresh(choice)
    return choice


# Привязать опцию к продукту
@router.post("/products/{product_id}/options/{option_id}")
def attach_option_to_product(
    product_id: int,
    option_id: int,
    data: ProductOptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPPORT]:
        raise HTTPException(status_code=403, detail="Not authorized")

    link = ProductOption(product_id=product_id, option_id=option_id, **data.dict())
    db.add(link)
    db.commit()
    return {"ok": True}
