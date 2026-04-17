from fastapi import FastAPI
from mockData import products
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def index():
    return "Hello, Welcome to FastAPI"

@app.get("/home")
def home():
    return "Hello, Welcome to Home Page"

@app.get("/products/{id}")
def get_products(id: int):
    for p in products:
        if p["id"] == id:
            return p
    return {"error": "Product not found"}

@app.get("/user")
def get_user(name: str):
    return f"Hello, {name}! Welcome to FastAPI"

@app.post("/create-product")
def create_product(product: dict):
    products.append(product)
    return products

@app.delete("/delete_product/{product_id}")
def delete_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            products.remove(p)
            return f"product of id {product_id} is deleted successfully"
    return {"error": "Product not found"}

class User(BaseModel):
    name: str
    age: int

class ResponseModel(BaseModel):
    name: str

@app.post("/create-user")
def create_user(user: User):
    return f"User {user.name} with age {user.age} is created successfully"

@app.post("/profile", response_model=ResponseModel)
def create_profile():
    return {
        "name": "John Doe",
        "age": 30
    }

