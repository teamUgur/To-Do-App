from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from auth import get_current_user, router
from database import engine
from dependency import db_dependency
import models, schemas

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

user_dependency = Annotated[dict, Depends(get_current_user)]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)

@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    return {"User": user}

@app.post('/items/', response_model=schemas.Item)
def create_item(
    item: schemas.CreateItem, db: db_dependency, 
    user: user_dependency
    ):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get('/items/', response_model=list[schemas.Item])
def read_all_items(
    user: user_dependency,
    db: db_dependency, skip: int = 0, limit: int = 100,
    ):
    query = select(models.Item).offset(skip).limit(limit)
    result = db.execute(query)
    return result.scalars().all()

@app.get('/items/{item_id}', response_model=schemas.Item)
def read_item(item_id: int, db: db_dependency, user: user_dependency,):
    query = select(models.Item).where(item_id == models.Item.id)
    item = db.scalar(query)
    if item == None:
        raise HTTPException(status_code=404, detail="Id not found")
    return item

@app.put('/items/{item_id}', response_model=schemas.Item)
def edit_item(
    item_id: int, item: schemas.CreateItem, 
    db: db_dependency, user: user_dependency,):
    query = select(models.Item).where(item_id == models.Item.id)
    item_db = db.scalar(query)
    if item_db == None:
        raise HTTPException(status_code=404, detail="Id not found")

    for key, value in item.model_dump().items():
        setattr(item_db, key, value)

    db.commit()
    db.refresh(item_db)
    return item_db

@app.delete('/items/{item_id}')
def delete_item(item_id: int, db: db_dependency, user: user_dependency,):
    query = select(models.Item).where(item_id == models.Item.id)
    item = db.scalar(query)
    if item == None:
        raise HTTPException(status_code=404, detail="Id not found")

    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}