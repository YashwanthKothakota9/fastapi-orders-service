import uuid
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, APIRouter
from starlette import status
from starlette.responses import Response

from orders.api.schemas import (
    GetOrderSchema,
    CreateOrderSchema,
    GetOrdersSchema,
)

from typing import Optional

router = APIRouter(prefix="/orders", tags=["orders"])
orders = []


@router.get("/", response_model=GetOrdersSchema)
def get_orders(cancelled: Optional[bool] = None, limit: Optional[int] = None):
    if cancelled is None and limit is None:
        return {"orders": orders}
    query_set = [order for order in orders]
    if cancelled is not None:
        if cancelled:
            query_set = [
                order
                for order in query_set
                if order["status"] == "cancelled"
            ]
        else:
            query_set = [
                order
                for order in query_set
                if order["status"] != "cancelled"
            ]
    if limit is not None and len(query_set) > limit:
        return {"orders": query_set[:limit]}
    return {"orders": query_set}


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema,
)
def create_order(order_details: CreateOrderSchema):
    order = order_details.model_dump()
    order["id"] = uuid.uuid4()
    order["created"] = datetime.now()
    order["status"] = "created"
    orders.append(order)
    return order


@router.get("/{order_id}", response_model=GetOrderSchema)
def get_order(order_id: UUID):
    for order in orders:
        if order["id"] == order_id:
            return order
    raise HTTPException(
        status_code=404, detail=f"Order with ID {order_id} not found")


@router.put("/{order_id}", response_model=GetOrderSchema)
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    for order in orders:
        if order["id"] == order_id:
            order.update(order_details.model_dump())
            return order
    raise HTTPException(
        status_code=404, detail=f"Order with ID {order_id} not found")


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_order(order_id: UUID):
    for index, order in enumerate(orders):
        if order["id"] == order_id:
            orders.pop(index)
            return
    raise HTTPException(
        status_code=404, detail=f"Order with ID {order_id} not found")


@router.post("/{order_id}/cancel", response_model=GetOrderSchema)
def cancel_order(order_id: UUID):
    for order in orders:
        if order["id"] == order_id:
            order["status"] = "cancelled"
            return order
    raise HTTPException(
        status_code=404, detail=f"Order with ID {order_id} not found")


@router.post("/{order_id}/pay", response_model=GetOrderSchema)
def pay_order(order_id: UUID):
    for order in orders:
        if order["id"] == order_id:
            order["status"] = "progress"
            return order
    raise HTTPException(
        status_code=404, detail=f"Order with ID {order_id} not found")
