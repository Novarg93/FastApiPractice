# app/schemas/categories.py
from pydantic import BaseModel

class CategoryRead(BaseModel):
    id: int
    name: str
    slug: str
    game_id: int
    model_config = {"from_attributes": True}
