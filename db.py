import os
from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import session, SQLModel, create_engine

DATABASE_URL = os.getenv("DATABASE_URL", sqlite:///comicstore.db)

connect_args = {"check_name_thread": False} if DATABASE_URL.startswith("sqlite") else {} 

engine = create_engine(DATABASE_URL, connect_args=connect_args)

