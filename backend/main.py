from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import engine, LocalSession
import models, schemas

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

@app.post('/items/', response_model=schemas.Item)
def create_item(item: schemas.CreateItem, db: Session = Depends(get_db)):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get('/items/', response_model=list[schemas.Item])
def read_all_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = select(models.Item).offset(skip).limit(limit)
    result = db.execute(query)
    return result.scalars().all()

@app.get('/items/{item_id}', response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    query = select(models.Item).where(item_id == models.Item.id)
    item = db.scalar(query)
    if item == None:
        raise HTTPException(status_code=404, detail="Id not found")
    return item

@app.put('/items/{item_id}', response_model=schemas.Item)
def edit_item(item_id: int, item: schemas.CreateItem, db: Session = Depends(get_db)):
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
def delete_item(item_id: int, db: Session = Depends(get_db)):
    query = select(models.Item).where(item_id == models.Item.id)
    item = db.scalar(query)
    if item == None:
        raise HTTPException(status_code=404, detail="Id not found")

    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}