from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Data model for POST/PUT requests
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool

# --- In-memory Database ---
items_db = {
    1: {"name": "Laptop", "price": 55000.0, "in_stock": True},
    2: {"name": "Keyboard", "price": 1200.0, "in_stock": True},
    3: {"name": "Mouse", "price": 600.0, "in_stock": False},
}

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on EC2!"}

# GET all items
@app.get("/items/")
def get_all_items():
    return {"items": items_db}

# GET item by ID
@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "item": items_db[item_id]}

# POST → Add item
@app.post("/items/")
def create_item(item: Item):
    new_id = max(items_db.keys()) + 1
    items_db[new_id] = item.model_dump()
    return {"message": "Item added", "item_id": new_id, "item": item}

# PUT → Update an item
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item.dict()
    return {"message": "Item updated", "item_id": item_id, "item": item}

# DELETE → Remove an item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": "Item deleted", "item_id": item_id}