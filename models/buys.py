from pydantic import BaseModel
from typing import List

class BuyItem(BaseModel):
    issue_id: int
    cantidad: int

class BuyCreate(BaseModel):
    customer_id: int
    items: List[BuyItem]

class Buy(BaseModel):
    id: int
    customer_id: int
    fecha: str
    total: float
    items: List[BuyItem]