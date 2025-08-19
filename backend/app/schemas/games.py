# app/schemas/games.py
from pydantic import BaseModel

class GameRead(BaseModel):
    id: int
    name: str
    slug: str
    model_config = {"from_attributes": True}
