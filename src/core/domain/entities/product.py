from datetime import time
from decimal import Decimal, ROUND_HALF_UP

from src.core.domain.enums.maintenance_time import MaintenanceTime


class Product:
    def __init__(
        self,
        id: int | None,
        name: str,
        api_id: str,
        uzname: str | None,
        runame: str | None,
        enname: str | None,
        description: str,
        img: str,
        image_url: str,
        img_file_id: str,
        price: Decimal,
        category_id: int,
        subcategory_index: int,
        branch_id: int,
        is_active: bool,
        maintenance_day: float | None,
        maintenance_night: float | None
    ):
        self.id = id
        self.name = name
        self.api_id = api_id
        self.uzname = uzname
        self.runame = runame
        self.enname = enname
        self.description = description
        self.img = img
        self.image_url = image_url
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

    
    def update_base_info(self, name: str, description: str, api_id: int) -> None:
        self.name = name
        self.description = description
        self.api_id = api_id

    def update_localization(self, uzname: str | None, runame: str | None, enname: str | None) -> None:
        self.uzname = uzname
        self.runame = runame
        self.enname = enname

    def update_images(self, image_url: str, img_file_id: str) -> None:
        self.image_url = image_url
        self.img_file_id = img_file_id

    def update_pricing(self, price: Decimal, maintenance_day: float | None, maintenance_night: float | None) -> None:
        self.price = price
        self.maintenance_day = maintenance_day
        self.maintenance_night = maintenance_night

    def update_categorization(self, category_id: int, subcategory_index: int, branch_id: int) -> None:
        self.category_id = category_id
        self.subcategory_index = subcategory_index
        self.branch_id = branch_id

    def change_status(self, is_active: bool) -> None:
        self.is_active = is_active