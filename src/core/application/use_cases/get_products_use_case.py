from src.core.domain.interfaces.product_repo import ProductRepository
from src.core.application.use_cases.dtos.product_dtos import ProductsDTO, GetProductsDTO, ProductDTO, GetProductsDTO

class GetProductsUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo
    
    async def execute(self, get_products_dto: GetProductsDTO) -> ProductsDTO:
        category_id = get_products_dto.category_id
        limit = get_products_dto.limit
        offset = get_products_dto.offset
        
        product_entities = await self.product_repo.get_list(
             category_id=category_id,
            limit=limit,
            offset=offset
        )
        
        product_dto_list = [
            ProductDTO(
                id=product.id,
                name=product.name,
                api_id=product.api_id,
                uzname=product.uzname,
                runame=product.runame,
                enname=product.enname,
                description=product.description,
                img=product.img,
                image_url=product.image_url,
                price=product.price,
                category_id=product.category_id,
                subcategory_index=product.subcategory_index,
                branch_id=product.branch_id,
                is_active=product.is_active,
                maintenance_day=product.maintenance_day,
                maintenance_night=product.maintenance_night
            )
            for product in product_entities
        ]
        return ProductsDTO(products=product_dto_list)
