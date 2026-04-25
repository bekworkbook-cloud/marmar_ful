from decimal import Decimal
from src.core.domain.exceptions.validation import DomainValidationError

class Order:
    def __init__(
        self,
        id: int | None,
        customer_id: int,
        operator_id: int | None,
        courier_id: int | None,
        branch_id: int,
        status: str,
        pay_method: str,
        total_price: Decimal,
        address: str,
        landmark: str,
        latitude: float,
        longitude: float
    ):
        if not (-90.0 <= latitude <= 90.0):
            raise DomainValidationError("Latitude must be between -90 and 90 degrees")
        
        if not (-180.0 <= longitude <= 180.0):
            raise DomainValidationError("Longitude must be between -180 and 180 degrees")
            
        if total_price < Decimal("0"):
            raise DomainValidationError("Total price cannot be negative")

        self.id = id
        self.customer_id = customer_id
        self.operator_id = operator_id
        self.courier_id = courier_id
        self.branch_id = branch_id
        self.status = status
        self.pay_method = pay_method
        self.total_price = total_price
        self.address = address
        self.landmark = landmark
        self.latitude = latitude
        self.longitude = longitude