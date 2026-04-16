from fastapi import FastAPI
from mockData import products

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

