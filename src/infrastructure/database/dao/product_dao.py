from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.models.product import Product as ProductModel

class ProductDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, product: ProductModel) -> ProductModel:
        self.session.add(instance=product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def get_by_id(self, product_id: int) -> ProductModel | None:
        result = await self.session.execute(
            select(ProductModel).where(ProductModel.id == product_id)
        )
        return result.scalar_one_or_none()

    async def update(self, product: ProductModel) -> ProductModel:
        merged_product = await self.session.merge(product)
        await self.session.commit()
        await self.session.refresh(merged_product)
        return merged_product
    
    async def delete(self, product_id: int) -> ProductModel:
        result = await self.session.execute(
            delete(ProductModel)
            .where(ProductModel.id == product_id)
        )
        await self.session.commit()
        return result.rowcount > 0

    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[ProductModel]:
        query = select(ProductModel)
        
        if filters:
            query = query.filter_by(**filters)
        
        result = await self.session.execute(
            query.order_by(ProductModel.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
