from decimal import Decimal
from datetime import datetime

from src.core.domain.exceptions.validation import DomainValidationError


class PaymentLog:
    def __init__(
            self,
            id: int,
            order_id: int,
            courier_id: int,
            branch_id: int,
            amount: Decimal,
            status: str,
            payment_method: str,
            is_closed: bool = False,
            create_at: datetime = None,
        ):


        self.id=id
        self.order_id=order_id
        self.courier_id=courier_id
        self.branch_id=branch_id
        self.amount=amount
        self.status=status
        self.payment_method=payment_method
        self.is_closed=is_closed
        self.created_at=create_at

        if self.amount<0:
            raise DomainValidationError("Negetiv amount value")
        if self.payment_method is None:
            raise DomainValidationError("Payment method none value")
        