from fastapi import FastAPI

app = FastAPI()

# Temporary in-memory cart storage
cart = []

@app.get("/")
def home():
    return {"message": "Cart Service Running"}

@app.get("/cart")
def get_cart():
    return {"cart_items": cart}

@app.post("/cart/add/{product_id}")
def add_to_cart(product_id: int):
    cart.append({"product_id": product_id})
    return {"message": "Item added to cart", "cart": cart}

@app.post("/cart/remove/{product_id}")
def remove_from_cart(product_id: int):
    global cart
    cart = [item for item in cart if item["product_id"] != product_id]
    return {"message": "Item removed", "cart": cart}

