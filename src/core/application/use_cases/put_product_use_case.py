from src.core.domain.interfaces.product_repo import ProductRepository
from src.core.application.use_cases.dtos.product_dtos import ProductDTO, ProductUpdateDTO


class PutProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def execute(self, product_update_dto: ProductUpdateDTO) -> ProductDTO:
        product_entity = await self.product_repo.get_by_id(product_id=product_update_dto.product_id)


        product_entity.update_base_info(
            name=product_update_dto.name,
            description=product_update_dto.description,
            api_id=None
        )

        product_entity.update_localization(
            uzname=None,
            runame=None,
            enname=None
        )

        product_entity.update_images(
            img=None,
            image_url=None,
            img_file_id=None
        )

        product_entity.update_pricing(
            price=product_update_dto.price,
            maintenance_day=product_update_dto.maintenance_day,
            maintenance_night=product_update_dto.maintenance_night
        )

        product_entity.update_categorization(
            category_id=product_update_dto.category_id,
            subcategory_index=None,
            branch_id=product_update_dto.branch_id
        )

        product_entity.change_status(
            is_active=product_update_dto.is_active
        )