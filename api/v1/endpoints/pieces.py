from fastapi import APIRouter, Request, Form, HTTPException
from sqlmodel import select
from ....db.models import Piece
from ....db.session import SessionDep
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter()

@router.get("/", status_code=200)
async def get_all_pieces(session:SessionDep):
	pieces = session.exec(select(Piece).order_by(Piece.name)).all()
	return {"Message": pieces}

@router.get("/{piece_id}", status_code=200)
async def get_piece(session:SessionDep, piece_id:int):
	db_piece = session.exec(select(Piece).where(Piece.id==piece_id)).first()
	if not db_piece:
		raise HTTPException(status_code=404, detail="Piece not found")
	return db_piece

@router.post("/add", status_code=204)
async def create_new_piece(session:SessionDep, name:str, level:int):
	db_piece = Piece(name=name, level=level)
	session.add(db_piece)
	session.commit()
	session.refresh(db_piece)
	return

@router.post("/edit", status_code=200)
async def edit_piece(session:SessionDep, id:int, name:str, nickname:str, level:int):
	db_piece = session.exec(select(Piece).where(Piece.id==id)).first()
	if not db_piece:
		raise HTTPException(status_code=404, detail="Piece not found")
	db_piece.name = name
	db_piece.nickname = nickname
	db_piece.level = level
	session.commit()
	session.refresh(db_piece)
	return {"Message": db_piece}

@router.post("/delete", status_code=204)
async def delete_piece(session:SessionDep, id:int):
	db_piece = session.exec(select(Piece).where(Piece.id==id)).first()
	if not db_piece:
		raise HTTPException(status_code=404, detail="Piece not found")
	session.delete(db_piece)
	session.commit()
	return
