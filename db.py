import os
from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///comicstore.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {} 

engine = create_engine(DATABASE_URL, connect_args=connect_args)

def create_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
