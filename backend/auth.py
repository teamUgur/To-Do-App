import os
from datetime import datetime, timezone, timedelta
from typing import Annotated

from fastapi import Router, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from dotenv import load_dotenv
from passlib.context import CryptContext
from sqlalchemy import select

from models import User
from dependency import db_dependency

load_dotenv()

router = Router(prefix="/auth", tags=['auth'])

SECRET_KEY=os.getenv('SECRET_KEY')
ALGORITHM=os.getenv('ALGORITHM')

crypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
password_bearer = OAuth2PasswordBearer(tokenurl='auth/token')

class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def authenticate_user(username: str, password: str, db):
    query = select(User).where(User.username == username)
    user = db.scalar(query)

    if not user:
        return False
    if not crypt_context (password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, expire_time: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + timedelta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated(str, Depends(password_bearer))):
    try: 
        payload = jwt.decode(token,SECRET_KEY, algorithm=[ALGORITHM])
        username: str | None = payload.get('sub')
        user_id: int | None = payload.get('id')

        if not username or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not verify the user"
            )
    except JWTError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not verify the user"
            )