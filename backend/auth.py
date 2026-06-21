import os
from datetime import datetie, timezone, timedelta
from typing import Annotated

from fastapi import Router, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWSError, jwt
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

