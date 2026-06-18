from fastapi import FastAPI, Depends, HTPPExcept
from sqlalchemy import Session
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal 
import models, schemas

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin=["http://localhost:3000"],
    allow_credenrials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()