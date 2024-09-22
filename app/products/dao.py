from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.products.models import Product
from app.products.schemas import ProductCreate, ProductUpdate


class ProductDAO:
    @staticmethod
    async def create_product(db: AsyncSession, product_data: ProductCreate):
        """
        Create a new product.

        Args:
            db (AsyncSession): The database session.
            product_data (ProductCreate): The product data to create the product with.

        Returns:
            Product: The newly created product.
        """
        new_product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            available=product_data.available,
        )
        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)
        return new_product

    @staticmethod
    async def get_all_products(db: AsyncSession):
        """
        Get all products.

        Args:
            db (AsyncSession): The database session.

        Returns:
            List[Product]: A list of all products.
        """

        result = await db.execute(select(Product))
        return result.scalars().all()

    @staticmethod
    async def get_product_by_id(db: AsyncSession, id: int):
        """
        Get a product by id.

        Args:
            db (AsyncSession): The database session.
            id (int): The product id.

        Returns:
            Product: The product if found, otherwise None.
        """

        return await db.get(Product, id)

    @staticmethod
    async def update_product(db: AsyncSession, id: int, product_update: ProductUpdate):
        """
        Update a product by id.

        Args:
            db (AsyncSession): The database session.
            id (int): The product id.
            product_update (ProductUpdate): The product data to update the product with.

        Returns:
            Product: The updated product if found, otherwise None.
        """
        product = await db.get(Product, id)
        if not product:
            return None
        for field, value in product_update.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def delete_product(db: AsyncSession, id: int):
        """
        Delete a product by id.

        Args:
            db (AsyncSession): The database session.
            id (int): The product id.

        Returns:
            bool: True if the product was found and deleted, otherwise None.
        """

        product = await db.get(Product, id)
        if not product:
            return None
        await db.delete(product)
        await db.commit()
        return True
