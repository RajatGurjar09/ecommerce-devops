from fastapi import FastAPI, Request, HTTPException
import requests

app = FastAPI(title="API Gateway")

PRODUCT_SERVICE = "http://product-service:8001"
CART_SERVICE = "http://cart-service:8002"
ORDER_SERVICE = "http://order-service:8003"


@app.get("/health")
def health():
    return {"status": "API Gateway is healthy"}


# -------- Product Routes --------
@app.get("/products")
def get_products():
    r = requests.get(f"{PRODUCT_SERVICE}/products")
    return r.json()


# -------- Cart Routes --------
@app.post("/cart/add/{product_id}")
def add_to_cart(product_id: int):
    r = requests.post(f"{CART_SERVICE}/cart/add/{product_id}")
    return r.json()


@app.get("/cart")
def get_cart():
    r = requests.get(f"{CART_SERVICE}/cart")
    return r.json()


# -------- Order Routes --------
@app.post("/order/from-cart")
def create_order():
    r = requests.post(f"{ORDER_SERVICE}/order/from-cart")
    if r.status_code != 200:
        raise HTTPException(status_code=500, detail="Order creation failed")
    return r.json()


@app.get("/orders")
def get_orders():
    r = requests.get(f"{ORDER_SERVICE}/orders")
    return r.json()

