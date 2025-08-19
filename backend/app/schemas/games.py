# app/schemas/games.py
from pydantic import BaseModel

class GameBase(BaseModel):
    name: str
    slug: str
    image: str
    description: str

    model_config = {"from_attributes": True}

class GameRead(GameBase):
    id: int
