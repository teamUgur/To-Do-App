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

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_request = User (
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password)
    )
    db.add(create_user_request)
    db.commit()

@router.post('/token', response_model=Token)
async def login_access_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate the user"
        )
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {"token": token, "token_type": bearer}