from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    price: float
    image: str | None = None
    quantity: int | None = None
    quality: int | None = None

    model_config = {
        "from_attributes": True
    }

class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class ItemListResponse(BaseModel):
    items: list[ItemRead]
    total: int

    model_config = {
        "from_attributes": True
    }
