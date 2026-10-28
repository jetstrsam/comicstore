from pydantic import BaseModel

class UserBase(BaseModel):
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

Class CustomerUpdate(BaseModel):
    nombres: str | None = None
    apellidos: str | None = None
    cc: str | None = None
    telefono: str | None = None
    email: str | None = None
    direccion: str | None = None
    membresia: str | None = None
