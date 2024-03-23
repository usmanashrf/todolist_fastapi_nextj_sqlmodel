from datetime import timedelta
import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter
from sqlalchemy import create_engine
from sqlmodel import Session, select
from passlib.context import CryptContext
from ..models import User, Token
from ..authorization import create_access_token
from ..database import get_session, engine

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
load_dotenv()

db_url = os.environ.get("DATABASE_URL")

def authenticate_user(email: str, password: str):
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        if not user:
            return False
        if not pwd_context.verify(password, user.password):
            return False
        return user

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/signup", response_model=User)
def signup(user_create: User, db: Annotated[Session, Depends(get_session)]):
    statement = select(User).where(User.username == user_create.username)
    db_user = db.exec(statement).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user = User(username=user_create.username, password=hash_password(user_create.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=Token)
def login(user_credentials: User, db: Annotated[Session, Depends(get_session)]):
    statement = select(User).where(User.username == user_credentials.username)
    user = db.exec(statement).first()
    if not user or not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username}, user_id=user.id)
    return {"access_token": access_token, "token_type": "bearer"}
