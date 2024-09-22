from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.orders.schemas import OrderCreateSchema, OrderSchema, OrderPatchResponseSchema
from app.orders.dao import OrderDAO

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderSchema, status_code=201)
async def create_order(order_data: OrderCreateSchema, db: AsyncSession = Depends(get_db)):
    """
    Create a new order.

    Args:
        order_data (OrderCreateSchema): The data to create the order with.

    Returns:
        OrderSchema: The newly created order.

    Raises:
        HTTPException: If a product is not found or not enough in stock.
    """
    
    new_order = await OrderDAO.create_order(db, order_data)
    return new_order


@router.get("/", response_model=list[OrderSchema])
async def get_orders(db: AsyncSession = Depends(get_db)):
    """
    Get all orders.

    Returns:
        list[OrderSchema]: A list of all orders.
    """
    orders = await OrderDAO.get_all_orders(db)
    return orders


@router.get("/{id}", response_model=OrderSchema)
async def get_order_by_id(id: int, db: AsyncSession = Depends(get_db)):
    """
    Get an order by id.

    Args:
        id (int): The order id.

    Returns:
        OrderSchema: The order if found, otherwise raises a 404 HTTPException.

    Raises:
        HTTPException: If the order is not found.
    """
    order = await OrderDAO.get_order_by_id(db, id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch("/{id}/{status}", response_model=OrderPatchResponseSchema)
async def update_order(id: int, status: str, db: AsyncSession = Depends(get_db)):
    """
    Update an order status by id.

    Args:
        id (int): The order id.
        status (str): The new order status.

    Returns:
        OrderPatchResponseSchema: The updated order if found, otherwise raises a 404 HTTPException.

    Raises:
        HTTPException: If the order is not found.
    """
    order = await OrderDAO.update_order_status(db, id, status)
    if not order:
        raise HTTPException(status_code=411, detail="Order not found")
    return order


@router.delete("/{id}", status_code=204)
async def delete_order(id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete an order by id.

    Args:
        id (int): The order id.

    Returns:
        None: If the order is found and deleted.

    Raises:
        HTTPException: If the order is not found.
    """
    result = await OrderDAO.delete_order(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return result
