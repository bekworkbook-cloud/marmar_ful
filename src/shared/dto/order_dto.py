from pydantic import BaseModel
from typing import Optional
from src.shared.dto.order_item_dto import OrderItemCreateDTO
        

class OrderDTO(BaseModel):
    id: int
    customer_id: int
    operator_id: int
    courier_id: int
    branch_id: int
    status: str
    payment_method: str
    total_price: float
    is_accepted: bool
    address: str
    landmark: str
    latitude: float
    longitude: float

class OrderCreate(BaseModel):
    customer_id: int
    operator_id: int
    courier_id: int  
    branch_id: int  
    status: str
    payment_method: str
    total_price: float
    is_accepted: bool
    address: str
    landmark: str
    latitude: float  
    longitude: float
    order_items: list[OrderItemCreateDTO]
