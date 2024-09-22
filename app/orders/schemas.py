from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List


class OrderItemBaseSchema(BaseModel):
    product_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class OrderCreateSchema(BaseModel):
    status: str
    items: List[OrderItemBaseSchema]

    model_config = ConfigDict(from_attributes=True)


class OrderItemSchema(BaseModel):
    id: int
    product_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class OrderSchema(BaseModel):
    id: int
    date_created: datetime
    status: str
    items: List[OrderItemSchema]

    model_config = ConfigDict(from_attributes=True)


class OrderPatchResponseSchema(BaseModel):
    date_created: datetime
    status: str
    id: int

    model_config = ConfigDict(from_attributes=True)
