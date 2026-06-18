from fastapi import FastAPI, Depends, HTPPException
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

@app.post('/items/', respomse_model=schemas.Item)
def create_item(item: schemas.CreateItem, db: Session = Depends(get_db)):
    item_id = models.Item(**item.dict())
    db.add(item_id)
    db.commit()
    db.refresh(item_id)
    return item_id

@app.get('/items/', response_model=list[schemas.Item])
def read_all_items(skip: 0, limit: 100, db: Session = Depends(get_db)):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items

@app.get('/items/{item_id}', response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(item_id == models.Item.id).first()
    if item == None:
        raise HTTPException(status_code=404, detail='Item not found')
    return item

@app.put('/items/{item_id}', response_model=schema.Item)
def edit_item(item_id: int, item: schemas.CreateItem, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item == None:
        raise HTTPException(status_code=404, detail='Item not found')
    
    for key, value in item.dict().items():
        setattr(db.item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete('/items/{item_id}', respose_model=schemas.Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item == None:
        raise HTTPException(status_code=404, detail='Item not found')
    
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}