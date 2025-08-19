from pydantic import BaseModel

class ItemSearchResponse(BaseModel):
    id: int
    name: str
    price: float
    image: str | None
    game: str
    category: str