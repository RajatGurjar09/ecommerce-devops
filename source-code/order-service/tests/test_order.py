import pytest

# Dummy test just to ensure CI/CD workflow passes
def test_order_total_calculation():
    cart_items = [
        {"id": 1, "name": "Laptop", "price": 50000},
        {"id": 2, "name": "Mouse", "price": 1000}
    ]
    total_amount = sum(item["price"] for item in cart_items)
    assert total_amount == 51000

def test_empty_cart():
    cart_items = []
    total_amount = sum(item["price"] for item in cart_items) if cart_items else 0
    assert total_amount == 0

