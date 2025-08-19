from pydantic import BaseModel
from typing import List, Optional

class ItemSearchResponse(BaseModel):
    id: int
    name: str
    price: float
    image: Optional[str] = None

class SearchResponse(BaseModel):
    total: int
    items: List[ItemSearchResponse]