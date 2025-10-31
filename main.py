from contextlib import asynccontextmanager
from .db.session import create_db_and_tables, SessionDep
from .db.models import User
from sqlmodel import Field, SQLModel, Relationship, select
from fastapi import FastAPI
from .api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the DB
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1")
