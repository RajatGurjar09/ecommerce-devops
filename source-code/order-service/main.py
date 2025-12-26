import requests
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db, engine
from models import Order, OrderItem, Base
from logger import get_logger

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
logger = get_logger("order-service")

CART_SERVICE_URL = "http://cart-service:8002"


@app.get("/health")
def health():
    return {"status": "order-service healthy"}


@app.post("/order/from-cart")
def create_order_from_cart(db: Session = Depends(get_db)):
    try:
        logger.info("Fetching cart items")

        resp = requests.get(f"{CART_SERVICE_URL}/cart")
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch cart")

        cart_items = resp.json().get("cart", [])

        if not cart_items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        total_amount = sum(item["price"] for item in cart_items)

        order = Order(total_amount=total_amount)
        db.add(order)
        db.commit()
        db.refresh(order)

        for item in cart_items:
            db.add(
                OrderItem(
                    order_id=order.id,
                    product_id=item["id"],
                    product_name=item["name"],
                    product_price=item["price"],
                )
            )

        db.commit()

        logger.info(f"Order {order.id} created successfully")

        return {
            "message": "Order created successfully",
            "order_id": order.id,
            "total": total_amount,
            "items": cart_items,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Order creation failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()

    return [
        {
            "order_id": o.id,
            "total": o.total_amount,
            "items": [
                {
                    "id": i.product_id,
                    "name": i.product_name,
                    "price": i.product_price,
                }
                for i in o.items
            ],
        }
        for o in orders
    ]

