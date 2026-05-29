

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
    