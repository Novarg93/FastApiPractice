from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    image: str | None = None
    quantity: int | None = None
    quality: str | None = None

class ItemCreate(BaseModel):
    pass

class ItemRead(BaseModel):
    id: int

    class Config:
        orm_mode = True

