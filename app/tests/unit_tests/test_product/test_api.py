from httpx import AsyncClient
import pytest


# Products
@pytest.mark.asyncio
async def test_create_product(ac: AsyncClient):
    response = await ac.post(
        "/products/",
        json={
            "id": 1,
            "name": "Apple",
            "description": "tasty",
            "price": "100.00",
            "available": 5,
        },
    )
    print(response.text)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_products(ac: AsyncClient):
    response = await ac.get("/products/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_product(ac: AsyncClient):
    response = await ac.get("/products/1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_product(ac: AsyncClient):
    response = await ac.put(
        "/products/1",
        json={
            "id": 1,
            "name": "Apple",
            "description": "tasty",
            "price": "100.00",
            "available": 5,
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_product(ac: AsyncClient):
    response = await ac.delete("/products/1")
    assert response.status_code == 204


# Orders
@pytest.mark.asyncio
async def test_create_order(ac: AsyncClient):
    response = await ac.post(
        "/orders/",
        json={"status": "RECEIVED", "items": [{"product_id": 2, "quantity": 1}]},
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_orders(ac: AsyncClient):
    response = await ac.get("/orders/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_order(ac: AsyncClient):
    response = await ac.get("/orders/1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_order(ac: AsyncClient):
    response = await ac.patch("/orders/1/RECEIVED")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_order(ac: AsyncClient):
    response = await ac.delete("/orders/1")
    assert response.status_code == 204
