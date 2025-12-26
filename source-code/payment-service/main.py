from fastapi import FastAPI, HTTPException
from logger import get_logger

app = FastAPI()
logger = get_logger("payment-service")


@app.get("/health")
def health():
    return {"status": "Payment service is healthy"}


@app.post("/payment/pay/{order_id}")
def pay(order_id: int):
    logger.info(f"Processing payment for order_id={order_id}")

    if order_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid order ID")

    return {
        "message": "Payment successful",
        "order_id": order_id,
        "status": "PAID"
    }

