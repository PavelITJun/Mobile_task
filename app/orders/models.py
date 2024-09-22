import datetime
from app.database import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import DateTime, ForeignKey, Integer, String
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.products.models import Product


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    date_created: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )
    status: Mapped[str] = mapped_column(String(100))

    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer)

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product", back_populates="order_items")
