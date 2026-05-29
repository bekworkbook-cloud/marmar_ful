from fastapi import UploadFile
from src.core.domain.interfaces.product_repo import ProductRepository
from src.core.application.use_cases.dtos.product_dtos import ProductDTO
from src.infrastructure.external_services.file_storage import IFileStorage
from src.core.application.exceptions.not_found_exception import NotFoundException
from src.config import settings

BASE_SITE_URL = settings.BASE_SITE_URL

class UploadProductImageUseCase:
    def __init__(self, product_repo: ProductRepository, file_storage: IFileStorage):
        self.product_repo = product_repo
        self.file_storage = file_storage

    async def execute(self, product_id: int, file: UploadFile) -> ProductDTO:
        product_entity = await self.product_repo.get_by_id(product_id)
        if not product_entity:
            raise NotFoundException(f"Product with id {product_id} not found")

        saved_path = await self.file_storage.save(file, directory=f"{BASE_SITE_URL}/media/products/{product_id}")
        
        product_entity.update_images(
            image_url=saved_path,
            img_file_id="" 
        )
        
        updated_entity = await self.product_repo.update(product_entity)
        
        return ProductDTO(
            id=updated_entity.id,
            name=updated_entity.name,
            api_id=updated_entity.api_id,
            uzname=updated_entity.uzname,
            runame=updated_entity.runame,
            enname=updated_entity.enname,
            description=updated_entity.description,
            image_url=updated_entity.image_url,
            img_file_id=updated_entity.img_file_id,
            price=updated_entity.price,
            category_id=updated_entity.category_id,
            subcategory_index=updated_entity.subcategory_index,
            branch_id=updated_entity.branch_id,
            is_active=updated_entity.is_active,
            maintenance_day=updated_entity.maintenance_day,
            maintenance_night=updated_entity.maintenance_night,
        )