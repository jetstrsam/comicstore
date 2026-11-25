from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

class UserBase(SQLModel):
    nombres: str
    apellidos: str
    cc: str
    telefono: str
    email: str

class CustomerCreate(UserBase):
    direccion: str
    membresia: str

class Customer(CustomerCreate):
    id: int

class CustomerUpdate(UserBase):
    nombres: str | None = None
    apellidos: str | None = None
    cc: str | None = None
    telefono: str | None = None
    email: str | None = None
    direccion: str | None = None
    membresia: str | None = None
