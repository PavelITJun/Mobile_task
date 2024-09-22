from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.orders.models import Order, OrderItem
from app.products.models import Product
from app.orders.schemas import OrderCreateSchema


class OrderDAO:
    @staticmethod
    async def create_order(db: AsyncSession, order_data: OrderCreateSchema):
        """
        Create a new order and subtract the quantity from the products.
        Args:
            db (AsyncSession): The database session.
            order_data (OrderCreateSchema): The order data to create the order with.
        Returns:
            Order: The newly created order with the items.
        Raises:
            HTTPException: If a product is not found or not enough in stock.
        """
        new_order = Order(status=order_data.status)
        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)

        for item in order_data.items:
            product = (
                (await db.execute(select(Product).where(Product.id == item.product_id)))
                .scalars()
                .first()
            )

            if not product:
                raise HTTPException(status_code=410, detail="Product not found")

            if product.available < item.quantity:
                raise HTTPException(
                    status_code=400, detail="Not enough products in stock"
                )

            product.available -= item.quantity
            db.add(product)

            order_item = OrderItem(
                order_id=new_order.id, product_id=item.product_id, quantity=item.quantity
            )
            db.add(order_item)

        await db.commit()
        await db.refresh(new_order)

        query = (
            select(Order)
            .where(Order.id == new_order.id)
            .options(selectinload(Order.items))
        )
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_all_orders(db: AsyncSession):
        """Get all orders with their items.
        Args:
            db (AsyncSession): The database session.
        Returns:
            List[Order]: A list of orders with their items.
        """
        query = select(Order).options(selectinload(Order.items))
        result = await db.execute(query)
        return result.unique().scalars().all()

    @staticmethod
    async def get_order_by_id(db: AsyncSession, id: int):
        
        """Get an order by id with its items.
        Args:
            db (AsyncSession): The database session.
            id (int): The order id.
        Returns:
            Order: The order with its items if found, otherwise None.
        """
        query = select(Order).where(Order.id == id).options(selectinload(Order.items))
        result = await db.execute(query)
        return result.unique().scalars().first()

    @staticmethod
    async def update_order_status(db: AsyncSession, id: int, status: str):
        
        """Update an order status by id.
        Args:
            db (AsyncSession): The database session.
            id (int): The order id.
            status (str): The new order status.
        Returns:
            Order: The updated order if found, otherwise None.
        """
        order = await db.get(Order, id)
        if not order:
            return None
        order.status = status
        await db.commit()
        await db.refresh(order)
        return order

    @staticmethod
    async def delete_order(db: AsyncSession, id: int):
        """Delete an order by id.
        Args:
            db (AsyncSession): The database session.
            id (int): The order id.
        Returns:
            bool: True if the order was found and deleted, otherwise None.
        """
        order = await db.get(Order, id)
        if not order:
            return None
        await db.delete(order)
        await db.commit()
        return True
