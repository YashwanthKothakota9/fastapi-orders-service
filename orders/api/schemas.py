from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class Size(Enum):
    small = "small"
    medium = "medium"
    big = "big"


class StatusEnum(Enum):
    created = "created"
    paid = "paid"
    progress = "progress"
    cancelled = "cancelled"
    dispatched = "dispatched"
    delivered = "delivered"


class OrderItemSchema(BaseModel, extra="forbid"):
    product: str
    size: Size
    quantity: Optional[int] = Field(default=1, ge=1)

    @field_validator("quantity")
    def quantity_non_nullable(cls, value):
        assert value is not None, "quantity may not be None"
        return value


class CreateOrderSchema(BaseModel, extra="forbid"):
    order: List[OrderItemSchema] = Field(..., min_length=1)


class GetOrderSchema(CreateOrderSchema):
    id: UUID
    created: datetime
    status: StatusEnum


class GetOrdersSchema(BaseModel):
    orders: List[GetOrderSchema]
