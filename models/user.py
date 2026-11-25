from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .buys import Buys

class UserBase(SQLModel):
    nombres: str
    apellidos: str
    cc: str
    telefono: str
    email: str
    direccion: str
    membresia: str

class Customer(UserBase, table=True):
    id: int | Nonce = Field(default=None, primary_key=True)
    buys: list["Buys"] = Relationship(back_populates="customer")

class CustomerCreate(UserBase):
    pass

class CustomerUpdate(SQLModel):
    nombres: str | None = None
    apellidos: str | None = None
    cc: str | None = None
    telefono: str | None = None
    email: str | None = None
    direccion: str | None = None
    membresia: str | None = None
