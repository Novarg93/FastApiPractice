from pydantic import BaseModel, field_validator
from typing import Literal, get_args
from app.schemas.options import OptionSchema

Quality = Literal[
    "exotic", "currency", "gear", "material", "weapon",
    "unique", "cosmetic", "map", "mount", "shader", "consumable", "pet", "other"
]

_ALLOWED = set(get_args(Quality)) - {"other"}


class ItemBase(BaseModel):
    name: str
    price: float
    image: str | None = None
    quantity: int | None = None
    quality: Quality | None = None

    model_config = {"from_attributes": True}

    @field_validator("quality", mode="before")
    @classmethod
    def normalize_quality(cls, v):
        if v is None:
            return None
        v = str(v).strip().lower()
        return v if v in _ALLOWED else "other"


class ItemCreate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: int
    options: list[OptionSchema] = []

    model_config = {
        "from_attributes": True
    }


class ItemListResponse(BaseModel):
    items: list[ItemRead]
    total: int

    model_config = {
        "from_attributes": True
    }