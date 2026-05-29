from src.core.domain.interfaces.product_repo import ProductRepository
from src.core.domain.entities.product import Product
from src.core.application.use_cases.dtos.product_dtos import ProductDTO, ProductCreateDTO

class PostProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def execute(self, product_create_dto: ProductCreateDTO) -> ProductDTO:
        product_entity = Product(
            id=None,
            name=product_create_dto.name,
            api_id=None,
            uzname=None,
            runame=None,
            enname=None,
            description=product_create_dto.description,
            img="",
            image_url="",
            img_file_id="",
            price=product_create_dto.price,
            category_id=product_create_dto.category_id,
            subcategory_index=0,
            branch_id=product_create_dto.branch_id,
            is_active=product_create_dto.is_active,
            maintenance_day=product_create_dto.maintenance_day,
            maintenance_night=product_create_dto.maintenance_day,
        )
        
        created_entity = await self.product_repo.add(product=product_entity)
        
        return ProductDTO(
            id=created_entity.id,
            name=created_entity.name,
            api_id=created_entity.api_id,
            uzname=created_entity.uzname,
            runame=created_entity.runame,
            enname=created_entity.enname,
            description=created_entity.description,
            img=created_entity.img,
            image_url=created_entity.image_url,
            img_file_id=created_entity.img_file_id,
            price=created_entity.price,
            category_id=created_entity.category_id,
            subcategory_index=created_entity.subcategory_index,
            branch_id=created_entity.branch_id,
            is_active=created_entity.is_active,
            maintenance_day=created_entity.maintenance_day,
            maintenance_night=created_entity.maintenance_night,
        )
