from pydantic import BaseModel

class IssueBase(BaseModel):
    titulo: str
    editorial: str
    precio: float
    stock: int
    esta_activo: bool = True
    

class IssueCreate(IssueBase):
    pass

class Issue(IssueBase):
    id: int

class IssueUpdate(BaseModel):
    titulo: str | None = None
    editorial: str | None = None
    precio: float | None = None
    stock: int | None = None
    esta_activo: bool | None = None