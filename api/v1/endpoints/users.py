from fastapi import APIRouter, Request, Form, HTTPException
from sqlmodel import select
from ....db.models import User
from ....db.session import SessionDep
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter()

@router.get("/", status_code=200)
async def get_all_users(session:SessionDep):
	users = session.exec(select(User).order_by(User.name)).all()
	return {"Message": users}

@router.get("/{user_id}", status_code=200)
async def get_user(session:SessionDep, user_id:int):
	db_user = session.exec(select(User).where(User.id==user_id)).first()
	if not db_user:
		raise HTTPException(status_code=404, detail="User not found")
	return db_user

@router.post("/add", status_code=204)
async def create_new_user(session:SessionDep, name:str, password:str):
	db_user = User(name=name, password=password)
	session.add(db_user)
	session.commit()
	session.refresh(db_user)
	return

@router.post("/edit", status_code=200)
async def edit_user(session:SessionDep, id:int, name:str, password:str, wins:int, losses:int):
	db_user = session.exec(select(User).where(User.id==id)).first()
	if not db_user:
		raise HTTPException(status_code=404, detail="User not found")
	db_user.name = name
	db_user.password = password
	db_user.wins = wins
	db_user.losses = losses
	session.commit()
	session.refresh(db_user)
	return {"Message": db_user}

@router.post("/delete", status_code=204)
async def delete_user(session:SessionDep, id:int):
	db_user = session.exec(select(User).where(User.id==id)).first()
	if not db_user:
		raise HTTPException(status_code=404, detail="User not found")
	session.delete(db_user)
	session.commit()
	return
