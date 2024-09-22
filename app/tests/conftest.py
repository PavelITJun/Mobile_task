import datetime
import json
import pytest_asyncio
from sqlalchemy import insert
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.orders.models import Order, OrderItem
from app.products.models import Product
from httpx import ASGITransport, AsyncClient
from main import app as fastapi_app


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mocks/{model}.json", encoding="UTF-8") as file:
            return json.load(file)

    products = open_mock_json("products")
    orders = open_mock_json("orders")
    order_items = open_mock_json("order_items")

    for order in orders:
        order["date_created"] = datetime.datetime.strptime(
            order["date_created"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )

    async with async_session_maker() as session:
        await session.execute(insert(Product).values(products))
        await session.execute(insert(Order).values(orders))
        await session.execute(insert(OrderItem).values(order_items))
        await session.commit()

    yield


@pytest_asyncio.fixture(scope="function")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://test/"
    ) as client:
        yield client
