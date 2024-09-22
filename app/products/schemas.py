from pydantic import BaseModel, ConfigDict
from decimal import Decimal


class ProductSchema(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    available: int

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    name: str
    description: str
    price: Decimal
    available: int

    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(BaseModel):
    name: str
    description: str
    price: Decimal
    available: int

    model_config = ConfigDict(from_attributes=True)


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    available: int

    model_config = ConfigDict(from_attributes=True)
