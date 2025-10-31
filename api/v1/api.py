from fastapi import APIRouter
from .endpoints import users, pieces, games

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(pieces.router, prefix="/pieces", tags=["Pieces"])
api_router.include_router(games.router, prefix="/games", tags=["Games"])
