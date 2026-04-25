from datetime import time
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum

class MaintenanceTime(Enum):
    DAY_START = time(7, 0)
    DAY_END = time(17, 0)

class Product:
    def __init__(
        self,
        id: int | None,
        name: str,
        api_id: int,
        uzname: str,
        runame: str,
        enname: str,
        desc: str,
        img: str,
        img_file_id: str,
        price: Decimal,
        category_id: int,
        subcategory_index: int,
        branch_id: int,
        is_active: bool,
        maintenance_day: int,
        maintenance_night: int
    ):
        self.id = id
        self.name = name
        self.api_id = api_id
        self.uzname = uzname
        self.runame = runame
        self.enname = enname
        self.desc = desc
        self.img = img
        self.img_file_id = img_file_id
        self.price = price
        self.category_id = category_id
        self.subcategory_index = subcategory_index
        self.branch_id = branch_id
        self.is_active = is_active
        self.maintenance_day = maintenance_day
        self.maintenance_night = maintenance_night

    def get_price(self, time_now: time) -> Decimal:
        if MaintenanceTime.DAY_START.value <= time_now <= MaintenanceTime.DAY_END.value:
            multiplier = Decimal('1') + Decimal(self.maintenance_day) / Decimal('100')
        else:
            multiplier = Decimal('1') + Decimal(self.maintenance_night) / Decimal('100')

        return (self.price * multiplier).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
