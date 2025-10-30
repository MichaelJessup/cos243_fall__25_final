from contextlib import asynccontextmanager
from .db.session import create_db_and_tables, SessionDep
from sqlmodel import Field, SQLModel, Relationship, select
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the DB
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    password: str
    wins: int | None
    losses: int | None
    winrate: float | None

class Piece(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    nickname: str | None
    level: int

class Game(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    p1_id: int | None = Field(default=None, foreign_key="user.id")
    p2_id: int | None = Field(default=None, foreign_key="user.id")
    pieces: list[Piece] | None = Relationship(back_populates="name")
