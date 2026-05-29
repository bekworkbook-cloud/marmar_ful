from src.core.domain.interfaces.product_repo import ProductRepository
from src.core.application.use_cases.dtos.product_dtos import ProductDTO, ProductUpdateDTO

class PatchProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def execute(self, product_id: ProductDTO, product_update: ProductUpdateDTO) -> ProductDTO:
        pass
        # product_entity = await self.product_repo.get_by_id(product_id=product_id.id)
        
        # product_entity.update_fields(
        #     name=product_update.name,
        #     category_id=product_update.category_id,
        #     branch_id=product_update.branch_id,
        #     description=product_update.description,
        #     price=product_update.price,
        #     is_active=product_update.is_active
        # )
        
        # updated_entity = await self.product_repo.update(product_entity)
        
        # return ProductDTO(
        #     id=updated_entity.id,
        #     name=updated_entity.name,
        #     category_id=updated_entity.category_id,
        #     branch_id=updated_entity.branch_id,
        #     description=updated_entity.description,
        #     price=updated_entity.price,
        #     is_active=updated_entity.is_active
        # )