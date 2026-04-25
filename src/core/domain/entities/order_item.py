from decimal import Decimal

from src.core.domain.exceptions.validation import DomainValidationError


class OrderItem:
    def __init__(
        self,
        id: int | None,
        order_id: int,
        product_id: int,
        quantity: int,
        price_at_purchase: Decimal
    ):
        if quantity <= 0:
            raise DomainValidationError("Quantity must be strictly greater than zero")
        
        if price_at_purchase < Decimal("0"):
            raise DomainValidationError("Price cannot be negative")

        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price_at_purchase = price_at_purchase

    def get_total_price(self) -> Decimal:
        return self.price_at_purchase * Decimal(self.quantity)