from fastapi import FastAPI, HTTPException, Request
import time

from logger import get_logger

app = FastAPI()
logger = get_logger()

products = [
    {"id": 1, "name": "Laptop", "price": 50000},
    {"id": 2, "name": "Phone", "price": 20000},
    {"id": 3, "name": "Headphones", "price": 3000},
]


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = round((time.time() - start_time) * 1000, 2)

    logger.info(
        "HTTP request processed",
        extra={
            "extra_data": {
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": process_time,
            }
        },
    )

    return response


@app.get("/")
def home():
    logger.info("Product service home endpoint called")
    return {"message": "Product Service Running"}


@app.get("/product/{product_id}")
def get_product(product_id: int):
    logger.info(
        "Fetching product",
        extra={"extra_data": {"product_id": product_id}},
    )

    for product in products:
        if product["id"] == product_id:
            logger.info(
                "Product found",
                extra={"extra_data": {"product_id": product_id}},
            )
            return product

    logger.warning(
        "Product not found",
        extra={"extra_data": {"product_id": product_id}},
    )

    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/health")
def health():
    return {"status": "ok", "service": "product-service"}

