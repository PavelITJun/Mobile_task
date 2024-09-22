from fastapi import APIRouter, HTTPException
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, status
from app.products.schemas import ProductCreate, ProductResponse, ProductUpdate
from app.products.dao import ProductDAO

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new product.

    Args:
        product (ProductCreate): The product data to create the product with.

    Returns:
        ProductResponse: The newly created product.

    Raises:
        HTTPException: If a database error occurs.
    """
    new_product = await ProductDAO.create_product(db, product)
    return new_product


@router.get("/", response_model=list[ProductResponse])
async def get_products(db: AsyncSession = Depends(get_db)):
    """
    Get all products.

    Returns:
        list[ProductResponse]: A list of all products.
    """
    products = await ProductDAO.get_all_products(db)
    return products


@router.get("/{id}", response_model=ProductResponse)
async def get_product(id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a product by id.

    Args:
        id (int): The product id.

    Returns:
        ProductResponse: The product if found, otherwise raises a 404 HTTPException.

    Raises:
        HTTPException: If the product is not found.
    """

    product = await ProductDAO.get_product_by_id(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{id}", response_model=ProductResponse)
async def update_product(
    id: int, product_update: ProductUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Update a product by id.

    Args:
        id (int): The product id.
        product_update (ProductUpdate): The product update data.

    Returns:
        ProductResponse: The updated product if found, otherwise raises a 404 HTTPException.

    Raises:
        HTTPException: If the product is not found.
    """
    product = await ProductDAO.update_product(db, id, product_update)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a product by id.

    Args:
        id (int): The product id.

    Returns:
        None: If the product was found and deleted.

    Raises:
        HTTPException: If the product is not found.
    """

    product = await ProductDAO.delete_product(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return None
