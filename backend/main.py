from database import engine, LocalSession
from sqlalchemy.orm import Session
import models, schemas
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:3000",
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
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get('/items/', response_model=list[schemas.Item])
def read_all_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    item = db.query(models.Item).offset(skip).limit(limit).all()
    return item

@app.get('/items/{item_id}', response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(item_id == models.Item.id).first()
    if item == None:
        raise HTTPException(status_code=404, detail="Id not found")
    return item

@app.put('/items/{item_id}', response_model=schemas.Item)
def edit_item(item_id: int, item: schemas.CreateItem, db: Session = Depends(get_db)):
    item_db = db.query(models.Item).filter(item_id == models.Item.id).first()
    if item_db == None:
        raise HTTPException(status_code=404, detail="Id not found")

    for key, value in item.dict().items():
        setattr(item_db, key, value)

    db.commit()
    db.refresh(item_db)
    return item_db

@app.delete('/items/{item_id}')
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(item_id == models.Item.id).first()
    if item == None:
        raise HTTPException(status_code=404, detail="Id not found")

    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}