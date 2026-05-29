from decimal import Decimal
from src.core.domain.exceptions.validation import DomainValidationError
from src.core.domain.enums.order_status import OrderStatus
from src.core.domain.enums.payment_method import PaymentMethods
from src.core.domain.entities.order_item import OrderItem

class Order:
    def __init__(
        self,
        id: int | None,
        customer_id: int,
        operator_id: int | None,
        courier_id: int | None,
        branch_id: int,
        status: OrderStatus, # статус заказа 
        payment_method: PaymentMethods,
        total_price: Decimal,
        is_accepted: bool, # подтверждение заказа оператором
        address: str,
        landmark: str,
        latitude: float,
        longitude: float
    ):
        self.id = id
        self.customer_id = customer_id
        self.operator_id = operator_id
        self.courier_id = courier_id
        self.branch_id = branch_id
        self.status = status
        self.payment_method = payment_method
        self.total_price = total_price
        self.is_accepted = is_accepted
        self.address = address
        self.landmark = landmark
        self.latitude = latitude
        self.longitude = longitude

        if not (-90.0 <= latitude <= 90.0):
            raise DomainValidationError("Latitude must be between -90 and 90 degrees")
        
        if not (-180.0 <= longitude <= 180.0):
            raise DomainValidationError("Longitude must be between -180 and 180 degrees")
            
        if total_price < Decimal("0"):
            raise DomainValidationError("Total price cannot be negative")
        
    def assign_personnel(self, operator_id: int | None, courier_id: int | None) -> None:
        self.operator_id = operator_id
        self.courier_id = courier_id

    def change_operator(self, operator_id: int | None) -> None:
        self.operator_id = operator_id
    
    def change_courier(self, courier_id: int | None) -> None:
        self.courier_id = courier_id

    def change_status(self, new_status: OrderStatus) -> None:
        self.status = new_status

    def change_accept(self, is_accepted: bool) -> None:
        self.is_accepted = is_accepted

    def update_payment_info(self, payment_method: PaymentMethods) -> None:
        self.payment_method = payment_method

    def change_branch(self, branch_id: int) -> None:
        self.branch_id = branch_id
        
    def update_order_items(self, order_items: list[OrderItem]) -> None:
        self.order_items = order_items
        
    def correct_delivery_address(self, address: str, landmark: str, latitude: float, longitude: float) -> None:
        self.address = address
        self.landmark = landmark
        self.latitude = latitude
        self.longitude = longitude
