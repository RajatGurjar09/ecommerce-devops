import os
import requests
from fastapi import FastAPI

app = FastAPI()

ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/pay/{order_id}")
def pay(order_id: int):
    orders = requests.get(f"{ORDER_SERVICE_URL}/orders").json()
    return {"message": "Payment successful", "order_id": order_id}

