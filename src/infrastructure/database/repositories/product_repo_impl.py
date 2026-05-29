from src.core.domain.interfaces.product_repo import ProductRepository
from src.core.domain.entities.product import Product
from src.infrastructure.database.models.product import Product as ProductModel
from src.infrastructure.database.dao.product_dao import ProductDAO

class ProductRepositoryImpl(ProductRepository):
    def __init__(self, product_dao: ProductDAO):
        self.product_dao = product_dao

    def _to_entity(self, model: ProductModel) -> Product:
        return Product(
            id=model.id,
            name=model.name,
            api_id=model.api_id,
            uzname=model.uzname,
            runame=model.runame,
            enname=model.enname,
            description=model.description,
            img=model.img,
            image_url=model.image_url,
            img_file_id=model.img_file_id,
            price=model.price,
            category_id=model.category_id,
            subcategory_index=model.subcategoryindex,
            branch_id=model.branch_id,
            is_active=model.is_active,
            maintenance_day=model.maintenance_day,
            maintenance_night=model.maintenance_night
        )

    def _to_model(self, entity: Product) -> ProductModel:
        return ProductModel(
            id=entity.id,
            name=entity.name,
            api_id=entity.api_id,
            uzname=entity.uzname,
            runame=entity.runame,
            enname=entity.enname,
            description=entity.description,
            img=entity.img,
            image_url=entity.image_url,
            img_file_id=entity.img_file_id,
            price=entity.price,
            category_id=entity.category_id,
            subcategoryindex=entity.subcategory_index,
            branch_id=entity.branch_id,
            is_active=entity.is_active,
            maintenance_day=entity.maintenance_day,
            maintenance_night=entity.maintenance_night
        )

    async def add(self, product: Product) -> Product:
        model = self._to_model(product)
        created_model = await self.product_dao.add(model)
        return self._to_entity(created_model)

    async def get_by_id(self, product_id: int) -> Product | None:
        model = await self.product_dao.get_by_id(product_id)
        if model is None:
            return None
        return self._to_entity(model)

    async def update(self, product: Product) -> Product:
        model = self._to_model(product)
        updated_model = await self.product_dao.update(model)
        return self._to_entity(updated_model)
    
    
    async def delete(self, product_id: int) -> None:
        return await self.product_dao.delete(product_id)

    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[Product]:
        models = await self.product_dao.get_list(limit=limit, offset=offset, **filters)
        return [self._to_entity(model) for model in models]