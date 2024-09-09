from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import db
import models
from schema import CriarItem, Item

app = FastAPI()

models.Base.metadata.create_all(bind=db.engine)


@app.get("/")
def home():
    pass


@app.post("/items/", response_model=Item)
def criar_item(item: CriarItem, db: Session = Depends(db.get_db)):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/items/", response_model=List[Item])
def ler_items(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db)):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items


@app.get("/items/{item_id}", response_model=Item)
def ler_item(item_id: int, db: Session = Depends(db.get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return db_item


@app.put("/items/{item_id}", response_model=Item)
def atualizar_item(item_id: int, item: CriarItem, db: Session = Depends(db.get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    for chave, valor in item.dict().items():
        setattr(db_item, chave, valor)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.delete("/items/{item_id}", response_model=Item)
def apagar_item(item_id: int, db: Session = Depends(db.get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    db.delete(db_item)
    db.commit()
    return db_item
