

from pydantic import BaseModel
from typing import Optional
        
class PaymentLogDTO(BaseModel):
    id: int
    order_id: int
    branch_id: int
    courier_id: int
    payment_method: str
    amount: float
    is_closed: bool

class PaymentLogCreateDTO(BaseModel):
    order_id: int
    branch_id: int
    courier_id: int
    payment_method: str = None
    amount: float = None
    is_closed: bool = False
    
class PaymentLogIdDTO(BaseModel):
    id: int

class GetPaymentLogsInputDTO(BaseModel):
    order_id: int
    branch_id: int
    courier_id: int
    limit: int
    offset: int

class PaymentLogsDTO(BaseModel):    
    payment_logs: list[PaymentLogDTO]

class PaymentLogUpdateDTO(BaseModel):
    order_id: int
    branch_id: int
    courier_id: int
    payment_method: str
    amount: float
    is_closed: bool = True