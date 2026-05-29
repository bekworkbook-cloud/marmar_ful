from src.core.domain.interfaces.product_repo import ProductRepository
from src.core.application.use_cases.dtos.product_dtos import GetProductDTO, ProductDTO

class GetProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def execute(self, get_product_dto: GetProductDTO) -> ProductDTO:
        product_entity = await self.product_repo.get_by_id(product_id=get_product_dto.product_id)
        return ProductDTO(
            id=product_entity.id,
            name=product_entity.name,
            api_id=product_entity.api_id,
            uzname=product_entity.uzname,
            runame=product_entity.runame,
            enname=product_entity.enname,
            description=product_entity.description,
            img=product_entity.img,
            image_url=product_entity.image_url,
            price=product_entity.price,
            category_id=product_entity.category_id,
            subcategory_index=product_entity.subcategory_index,
            branch_id=product_entity.branch_id,
            is_active=product_entity.is_active,
            maintenance_day=product_entity.maintenance_day,
            maintenance_night=product_entity.maintenance_night
        )

