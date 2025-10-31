from sqlmodel import Field, SQLModel, Relationship
from pydantic import BaseModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    password: str
    wins: int | None
    losses: int | None

class Piece(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    nickname: str | None
    level: int

class Game(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    p1_id: int | None = Field(default=None, foreign_key="user.id")
    p2_id: int | None = Field(default=None, foreign_key="user.id")
