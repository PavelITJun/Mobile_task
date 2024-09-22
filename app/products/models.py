from decimal import Decimal
from app.database import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import Integer, Numeric, String


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    available: Mapped[int] = mapped_column(Integer)

    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="product", cascade="all, delete-orphan"
    )


from app.orders.models import OrderItem
