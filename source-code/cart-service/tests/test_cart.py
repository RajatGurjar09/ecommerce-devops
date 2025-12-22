import pytest

# Dummy cart test
def test_add_to_cart():
    cart_items = []
    product = {"id": 1, "name": "Laptop", "price": 50000}
    cart_items.append(product)
    assert len(cart_items) == 1
    assert cart_items[0]["price"] == 50000

def test_empty_cart():
    cart_items = []
    assert len(cart_items) == 0

