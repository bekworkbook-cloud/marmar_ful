from pydantic import BaseModel

class OrderItemDTO(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price_at_purchase: float


class OrderItemCreateDTO(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price_at_purchase: float

class OrderItemsDTO(BaseModel):    
    items: list[OrderItemDTO]



class GetOrderItemsInputDTO(BaseModel):
    order_id: int
    limit: int
    offset: int
    current_user_id: int | None = None
    current_user_role: str | None = None