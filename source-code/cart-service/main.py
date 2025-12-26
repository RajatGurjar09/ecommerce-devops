import requests
import time
from fastapi import FastAPI, HTTPException
from logger import get_logger

app = FastAPI()
logger = get_logger()

PRODUCT_SERVICE_URL = "http://product-service:8001"

# In-memory cart (per service instance)
cart_items = []


@app.get("/health")
def health():
    return {"status": "ok", "service": "cart-service"}


@app.post("/cart/add/{product_id}")
def add_to_cart(product_id: int):
    start_time = time.time()

    logger.info(
        "Adding product to cart",
        extra={"extra_data": {"product_id": product_id}},
    )

    response = requests.get(f"{PRODUCT_SERVICE_URL}/product/{product_id}")

    if response.status_code != 200:
        logger.warning(
            "Product not found",
            extra={"extra_data": {"product_id": product_id}},
        )
        raise HTTPException(status_code=404, detail="Product not found")

    product = response.json()
    cart_items.append(product)

    duration = round((time.time() - start_time) * 1000, 2)

    logger.info(
        "Product added to cart",
        extra={
            "extra_data": {
                "cart_size": len(cart_items),
                "duration_ms": duration,
            }
        },
    )

    return {
        "message": "Product added to cart",
        "cart": cart_items,
    }


@app.get("/cart")
def get_cart():
    logger.info(
        "Fetching cart items",
        extra={"extra_data": {"cart_size": len(cart_items)}},
    )
    return {"cart_items": cart_items}


@app.post("/cart/clear")
def clear_cart():
    cart_items.clear()

    logger.info(
        "Cart cleared",
        extra={"extra_data": {"cart_size": 0}},
    )

    return {"message": "Cart cleared successfully"}

