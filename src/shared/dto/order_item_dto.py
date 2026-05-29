from pydantic import BaseModel
from typing import Optional

class OrderItemDTO(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price_at_purchase: float


class OrderItemCreateDTO(BaseModel):
    product_id: int
    quantity: int

class OrderItemsDTO(BaseModel):    
    order_items: list[OrderItemDTO]


class GetOrderItemsInputDTO(BaseModel):
    order_id: int
    limit: int
    offset: int

class OrderItemUpdateDTO(BaseModel):
    product_id: int
    quantity: int