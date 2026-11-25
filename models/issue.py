from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

from models.buys_issue_link import BuysIssueLink
from .buys import Buys

if TYPE_CHECKING:
    from .buys import Buys

class IssueBase(SQLModel):
    titulo: str
    editorial: str
    precio: float = Field(default=0.0, gt=0)
    stock: int = Field(default=0, ge=0)
    esta_activo: bool = True

class Issue(IssueBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    buys: list["Buys"] = Relationship(back_populates="issue", link_model=BuysIssueLink)

class IssueCreate(IssueBase):
    pass

class IssueUpdate(SQLModel):
    titulo: str | None = None
    editorial: str | None = None
    precio: float | None = None
    stock: int | None = None
    esta_activo: bool | None = None