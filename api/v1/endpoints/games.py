from fastapi import APIRouter, Request, Form, HTTPException
from sqlmodel import select
from ....db.models import Game
from ....db.session import SessionDep
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter()

@router.get("/", status_code=200)
async def get_all_games(session:SessionDep):
	games = session.exec(select(Game).order_by(Game.p1_id)).all()
	return {"Message": games}

@router.get("/{game_id}", status_code=200)
async def get_game(session:SessionDep, game_id:int):
	db_game = session.exec(select(Game).where(Game.id==game_id)).first()
	if not db_game:
		raise HTTPException(status_code=404, detail="Game not found")
	return db_game

@router.post("/add", status_code=204)
async def create_new_game(session:SessionDep, p1_id:int, p2_id:int):
	db_game = Game(p1_id=p1_id, p2_id=p2_id)
	session.add(db_game)
	session.commit()
	session.refresh(db_game)
	return

@router.post("/edit", status_code=200)
async def edit_game(session:SessionDep, id:int, p1_id:str, p2_id:int):
	db_game = session.exec(select(Game).where(Game.id==id)).first()
	if not db_game:
		raise HTTPException(status_code=404, detail="Game not found")
	db_game.p1_id = p1_id
	db_game.p2_id = p2_id
	session.commit()
	session.refresh(db_game)
	return {"Message": db_game}

@router.post("/delete", status_code=204)
async def delete_game(session:SessionDep, id:int):
	db_game = session.exec(select(Game).where(Game.id==id)).first()
	if not db_game:
		raise HTTPException(status_code=404, detail="Game not found")
	session.delete(db_game)
	session.commit()
	return
