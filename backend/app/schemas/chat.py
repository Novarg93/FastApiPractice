from pydantic import BaseModel, constr
from datetime import datetime

class MessageCreate(BaseModel):
    content: constr(min_length=1, max_length=1000)

class MessageRead(BaseModel):
    id: int
    sender_id: int
    content: str
    type: str
    created_at: datetime

    class Config:
        from_attributes = True