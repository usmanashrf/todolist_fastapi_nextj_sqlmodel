from fastapi import Depends, HTTPException, status
import jwt
from datetime import datetime, timedelta
from jwt import PyJWTError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select

from todo_core_apis.database import get_session
from todo_core_apis.models import User

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, user_id: int):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "user_id": user_id})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

security = HTTPBearer()


def get_current_user(token: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = decode_access_token(token.credentials)
    if token is None:
        raise credentials_exception
    username = token.get("sub")
    if username is None:
        raise credentials_exception
    statement = select(User).where(User.username == username)
    user = db.exec(statement).first()
    if user is None:
        raise credentials_exception
    return user