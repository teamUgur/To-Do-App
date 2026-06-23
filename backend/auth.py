import os
from datetime import datetime, timezone, timedelta
from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import select
from jose import jwt, JWTError
from dotenv import load_dotenv

from models import User
from dependency import db_dependency

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")

oauth_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_typr: str

def authenticate_user(username: str, password: str, db: db_dependency):
    query = select(User).where(User.username == username)
    user = db.scalar(query)

    if not user:
        return False
    if not crypt_context.verify(user.hashed_password, password):
        return False
    return user

def create_access_token(username: str, user_id: int, expire_time: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + timedelta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, crypt_context]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        user_id: int | None = payload.get("id")

        if not username or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Couldn't validate the user"
            )
    except JWTError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Couldn't validate the user"
            )

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    user = User(
        username=create_user_request.username,
        hashed_password=crypt_context.hash(create_user_request.password)
    )
    db.add(user)
    db.commit()

@router.post("token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Couldn't validate the user"
            )
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}