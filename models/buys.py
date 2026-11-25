from datetime import datetime, timezone
from typing import TYPE_CHECKING, List
from sqlmodel import Field, Relationship, SQLModel
from .buys_issue_link import BuysIssueLink

if TYPE_CHECKING:
    from .user import Customer
    from .issue import Issue

class BuysBase(SQLModel):
    fecha: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total: float = Field(default=0.0, ge=0)

class Buys(BuysBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    
    customer: "Customer" = Relationship(back_populates="buys")

    issue: list["Issue"] = Relationship(back_populates="buys", link_model=BuysIssueLink)

class BuyItem(SQLModel):
    issue_id: int
    cantidad: int = Field(default=1, gt=0)

class BuyCreate(SQLModel):
    customer_id: int
    items: List[BuyItem]

class Buy(BuysBase):
    id: int
    customer_id: int
    items: List[BuyItem]