# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory "database"
items = {}

# Data model
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI on EC2!"}

# Create item
@app.post("/items/")
def create_item(item_id: int, item: Item):
    if item_id in items:
        raise HTTPException(status_code=400, detail="Item already exists")
    items[item_id] = item
    return {"item_id": item_id, "item": item}

# Read item
@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "item": items[item_id]}

# Update item
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item
    return {"item_id": item_id, "item": item}

# Delete item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return {"message": f"Item {item_id} deleted"}
