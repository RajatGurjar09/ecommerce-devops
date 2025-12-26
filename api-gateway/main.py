import requests
from fastapi import FastAPI, Request, Response

app = FastAPI()

PRODUCT_SERVICE = "http://product-service:8001"
CART_SERVICE = "http://cart-service:8002"
ORDER_SERVICE = "http://order-service:8003"
PAYMENT_SERVICE = "http://payment-service:8004"


@app.get("/health")
def health():
    return {"status": "API Gateway is healthy"}


@app.api_route("/products/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_products(path: str, request: Request):
    return await proxy_request(request, f"{PRODUCT_SERVICE}/products/{path}")


@app.api_route("/cart/{path:path}", methods=["GET", "POST", "DELETE"])
async def proxy_cart(path: str, request: Request):
    return await proxy_request(request, f"{CART_SERVICE}/cart/{path}")


@app.api_route("/order/{path:path}", methods=["GET", "POST"])
async def proxy_order(path: str, request: Request):
    return await proxy_request(request, f"{ORDER_SERVICE}/order/{path}")


@app.api_route("/orders", methods=["GET"])
async def get_orders(request: Request):
    return await proxy_request(request, f"{ORDER_SERVICE}/orders")


@app.api_route("/payment/{path:path}", methods=["POST", "GET"])
async def proxy_payment(path: str, request: Request):
    return await proxy_request(request, f"{PAYMENT_SERVICE}/payment/{path}")


async def proxy_request(request: Request, url: str):
    body = await request.body()

    response = requests.request(
        method=request.method,
        url=url,
        headers={k: v for k, v in request.headers.items() if k.lower() != "host"},
        data=body,
        params=request.query_params,
    )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )

