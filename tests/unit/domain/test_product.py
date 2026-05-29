import pytest
from datetime import datetime, time
from decimal import Decimal, ROUND_HALF_UP
from src.core.domain.entities.product import Product
from src.core.domain.enums.maintenance_time import MaintenanceTime


def test_product():

    price = Decimal("100000.00")

    product = Product(
        id=1,
        name="Pirog",
        api_id=1234,
        uzname="isUzName",
        runame=None,
        enname=None,
        description="description",
        img="linkToImg",
        image_url="linkToImg",
        img_file_id="telegramImgFileId",
        price=price,
        category_id=32,
        subcategory_index=1,
        branch_id=1,
        is_active=True,
        maintenance_day=12.00,
        maintenance_night=15.00,
    )

    get_price_at_day = product.get_price(time(9, 0))
    get_price_at_night  = product.get_price(time(21, 0))


    price_with_maintenance_day = (
        price * (
            Decimal('1') + Decimal(product.maintenance_day) / Decimal('100')
        )
    ).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    price_with_maintenance_night = (
        price * (
            Decimal('1') + Decimal(product.maintenance_night) / Decimal('100')
            )
            ).quantize(Decimal('1'), rounding=ROUND_HALF_UP)


    assert product.id == 1
    assert product.name == "Pirog"
    assert product.api_id == 1234
    assert product.uzname == "isUzName"
    assert product.runame == None
    assert product.enname == None
    assert product.description == "description"
    assert product.img == "linkToImg"
    assert product.image_url == "linkToImg"
    assert product.img_file_id == "telegramImgFileId"
    assert product.price == price
    assert product.category_id == 32
    assert product.subcategory_index == 1
    assert product.branch_id == 1
    assert product.is_active == True
    assert get_price_at_day == price_with_maintenance_day
    assert get_price_at_night == price_with_maintenance_night
