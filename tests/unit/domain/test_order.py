import pytest

from decimal import Decimal

from src.core.domain.entities.order import Order, DomainValidationError, OrderStatus
from src.core.domain.enums.payment_method import PaymentMethods


def test_order():
    total_price = Decimal("230000.00")
    latitude = 41.31123214521312
    longitude = 69.23982068205171

    order = Order(
        id=1,
        customer_id=1234,
        operator_id=2341,
        courier_id=3412,
        branch_id=1,
        status=OrderStatus.CONFIRMED,
        payment_method=PaymentMethods.CASH,
        total_price=total_price,
        address="addresas",
        landmark="landmark",
        latitude=latitude,
        longitude=longitude,
        is_accepted=True
    )
    

    assert order.status==OrderStatus.CONFIRMED
    assert order.total_price==total_price
  
    assert order.latitude==latitude
    assert order.longitude==longitude


def test_order_wrong_longitude():
    total_price = Decimal("230000.00")
    latitude = 41.31123214521312
    longitude = 619.23982068205171

    with pytest.raises(DomainValidationError) as exc_info:

        order = Order(
            id=1,
            customer_id=1234,
            operator_id=2341,
            courier_id=3412,
            branch_id=1,
            status=OrderStatus.CONFIRMED,
            payment_method=PaymentMethods.CASH,
            total_price=total_price,
            address="addresas",
            landmark="landmark",
            latitude=latitude,
            longitude=longitude,
            is_accepted=True
        )

    assert str(exc_info.value) == "Longitude must be between -180 and 180 degrees"


def test_order_wrong_latitude():

    total_price = Decimal("230000.00")
    latitude = 141.31123214521312
    longitude = 69.23982068205171


    with pytest.raises(DomainValidationError) as exc_info:

        order = Order(
            id=1,
            customer_id=1234,
            operator_id=2341,
            courier_id=3412,
            branch_id=1,
            status=OrderStatus.CONFIRMED,
            payment_method=PaymentMethods.CASH,
            total_price=total_price,
            address="addresas",
            landmark="landmark",
            latitude=latitude,
            longitude=longitude,
            is_accepted=True
        )

    assert str(exc_info.value) == "Latitude must be between -90 and 90 degrees"


def test_order_with_negetive_total_price():

    total_price = Decimal("-230000.00")
    latitude = 41.31123214521312
    longitude = 69.23982068205171

    with pytest.raises(DomainValidationError) as exc_info:
        order = Order(
            id=1,
            customer_id=1234,
            operator_id=2341,
            courier_id=3412,
            branch_id=1,
            status=OrderStatus.CONFIRMED,
            payment_method=PaymentMethods.CASH,
            total_price=total_price,
            address="addresas",
            landmark="landmark",
            latitude=latitude,
            longitude=longitude,
            is_accepted=True
        )

    assert str(exc_info.value) == "Total price cannot be negative"