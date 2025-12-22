import requests
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db
from models import Order, OrderItem
from logger import get_logger

app = FastAPI()
logger = get_logger()

CART_SERVICE_URL = "http://cart-service:8002"

@app.get("/health")
def health():
    return {"status": "order-service healthy"}

@app.post("/order/from-cart")
def create_order_from_cart(db: Session = Depends(get_db)):
    try:
        logger.info("Fetching cart items from cart service")
        
        # Fetch cart items
        resp = requests.get(f"{CART_SERVICE_URL}/cart")
        if resp.status_code != 200:
            logger.error(f"Failed to fetch cart: {resp.status_code} {resp.text}")
            raise HTTPException(status_code=500, detail="Failed to fetch cart")

        cart_response = resp.json()
        cart_items = cart_response.get("cart_items", [])

        if not cart_items:
            logger.warning("Cart is empty")
            raise HTTPException(status_code=400, detail="Cart is empty")

        # Calculate total amount
        total_amount = sum(item["price"] for item in cart_items)

        # Create order with transaction
        try:
            order = Order(total_amount=total_amount)
            db.add(order)
            db.commit()
            db.refresh(order)

            # Add order items
            for item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item["id"],
                    product_name=item["name"],
                    product_price=item["price"]
                )
                db.add(order_item)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error: {str(e)}")
            raise HTTPException(status_code=500, detail="Order creation failed")

        # Optional: clear cart
        try:
            requests.post(f"{CART_SERVICE_URL}/cart/clear")
        except Exception as e:
            logger.warning(f"Failed to clear cart: {str(e)}")

        logger.info(f"Order created successfully: order_id={order.id}, total={total_amount}")
        return {
            "message": "Order created successfully",
            "order_id": order.id,
            "total": total_amount,
            "items": cart_items
        }

    except Exception as e:
        logger.error(f"Unhandled error in create_order_from_cart: {str(e)}")
        raise HTTPException(status_code=500, detail="Order creation failed")

