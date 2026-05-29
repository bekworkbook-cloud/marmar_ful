import pytest
from decimal import Decimal
from src.core.domain.entities.payment import PaymentLog, DomainValidationError

def test_payment_log_raises_error_on_negative_amount():
    negative_amount = Decimal("-100.00")
    
    with pytest.raises(DomainValidationError) as exc_info:
        PaymentLog(
            id=1,
            order_id=1,
            courier_id=1,
            status="pending",
            branch_id=1,
            amount=negative_amount,
            payment_method="click"
        )
    
    assert str(exc_info.value) == "Negetiv amount value"

def test_payment_log_success_with_positive_amount():
    amount = Decimal("50000.00")
    payment = PaymentLog(
        id=1,
        order_id=1,
        courier_id=1,
        status="pending",
        branch_id=1,
        amount=amount,
        payment_method="payme"
    )
    assert payment.amount == amount
