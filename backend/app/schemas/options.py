from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class OptionChoiceSchema(BaseModel):
    id: int
    value: str
    label: str
    pct: Optional[float] = None
    abs_cents: Optional[int] = None
    multiplier: Optional[float] = None
    sort_order: Optional[int] = None   # 🔑 переименовано под модель

    model_config = ConfigDict(from_attributes=True)


class OptionSchema(BaseModel):
    id: int
    name: str
    type: str
    label: str
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    step: Optional[int] = None

    choices: List[OptionChoiceSchema] = []

    model_config = ConfigDict(from_attributes=True)