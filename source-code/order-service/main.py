from fastapi import FastAPI

app = FastAPI()

# Temporary in-memory order list
orders = []

@app.get("/")
def home():
    return {"message": "Order Service Running"}

@app.post("/order/create/{product_id}")
def create_order(product_id: int):
    new_order = {"order_id": len(orders) + 1, "product_id": product_id, "status": "placed"}
    orders.append(new_order)
    return {"message": "Order created", "order": new_order}

@app.get("/orders")
def get_orders():
    return {"orders": orders}

