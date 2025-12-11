from fastapi import FastAPI

app = FastAPI()

# Temporary in-memory product list
products = [
    {"id": 1, "name": "Laptop", "price": 50000},
    {"id": 2, "name": "Headphones", "price": 2000},
    {"id": 3, "name": "Keyboard", "price": 1500},
]

@app.get("/")
def home():
    return {"message": "Product Service Running"}

@app.get("/products")
def get_products():
    return products

