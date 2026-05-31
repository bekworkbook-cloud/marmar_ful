from pydantic import BaseModel
from src.shared.dto.order_item_dto import OrderItemCreateDTO, OrderItemUpdateDTO
from typing import Optional


class OrderDTO(BaseModel):
    id: int
    customer_id: int
    operator_id: int | None = None
    courier_id: int | None = None
    branch_id: int
    status: str
    payment_method: str
    total_price: float
    is_accepted: bool
    address: str
    landmark: str | None = None
    latitude: float
    longitude: float


class OrderCreateInputDTO(BaseModel):
    branch_id: int
    payment_method: str
    address: str
    landmark: str | None = None
    latitude: float
    longitude: float
    order_items: list[OrderItemCreateDTO]


class OrderCreateDTO(BaseModel):
    branch_id: int  
    payment_method: str
    address: str
    landmark: str | None = None
    latitude: float  
    longitude: float
    current_user_id: int | None = None
    current_user_role: str | None = None
    order_items: list[OrderItemCreateDTO]


class OrderIdDTO(BaseModel):    
    id: int


class GetOrdersInputDTO(BaseModel):
    limit: int = 10
    offset: int = 0
    current_user_id: int | None = None
    current_user_role: str | None = None


class GetOrderInputDTO(BaseModel):
    id: int
    current_user_id: int | None = None
    current_user_role: str | None = None


class OrdersDTO(BaseModel):    
    items: list[OrderDTO]


class OrderUpdateDTO(BaseModel):
    order_id: Optional[int]
    branch_id: int
    payment_method: str
    address: str
    landmark: str | None = None
    latitude: float
    longitude: float
    current_user_id: Optional[int] = None
    current_user_role: Optional[str] = None
    # order_items: list[OrderItemUpdateDTO]


class OrderUpdateRequest(BaseModel):
    branch_id: int
    status: str
    payment_method: str
    is_accepted: bool = True
    address: str
    landmark: str | None = None
    latitude: float
    longitude: float
    # order_items: list[OrderItemUpdateDTO]


class UpdateOrderInputDTO(BaseModel):
    order_id: int
    branch_id: int
    payment_method: str
    address: str
    landmark: str | None = None
    latitude: float
    longitude: float
    is_accepted: bool = True
    # order_items: list[OrderItemUpdateDTO]
    current_user_id: int
    current_user_role: str


class OrderPersonnelUpdateDTO(BaseModel):
    courier_id: int | None = None
    operator_id: int | None = None
    order_id: int
    current_user_id: int
    current_user_role: str

class OrderPersonnelIdsDTO(BaseModel):
    courier_id: int
    operator_id: int 


class OrderCourierUpdateDTO(BaseModel):
    courier_id: int
    order_id: int


class OrderCourierUpdateDTO(BaseModel):
    courier_id: int
    order_id: int

class OrderOperatorUpdateDTO(BaseModel):
    operator_id: int
    order_id: int


class OrderPaymentUpdateDTO(BaseModel):
    payment_method: str
    order_id: int
    current_user_id: int
    current_user_role: str

class OrderPaymentMethodDTO(BaseModel):
    payment_method: str


class OrderStatusUpdateDTO(BaseModel):
    status: str
    order_id: int
    current_user_id: int
    current_user_role: str

class OrderStatusDTO(BaseModel):
    status: str


class OrderAcceptDTO(BaseModel):
    is_accepted: bool

class OrderAcceptUpdateDTO(BaseModel):
    is_accepted: bool
    order_id: int
    current_user_id: int
    current_user_role: str