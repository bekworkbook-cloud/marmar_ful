from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.models.category import Category as CategoryModel

class CategoryDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, category: CategoryModel) -> CategoryModel:
        self.session.add(instance=category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def count_all(self) -> int:
        result = await self.session.execute(
            select(func.count(CategoryModel.id))
        )
        return result.scalar() or 0
    
    async def count_by_branch_id(self, branch_id: int) -> int:
        result = await self.session.execute(
            select(func.count(CategoryModel.id))
            .where(CategoryModel.branch_id == branch_id)
        )
        return result.scalar() or 0
    
    async def get_by_id(self, category_id: int) -> CategoryModel | None:
        result = await self.session.execute(
            select(CategoryModel).where(CategoryModel.id == category_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self) -> list[CategoryModel]:
        result = await self.session.execute(
            select(CategoryModel)
        )
        return list(result.scalars().all())
    
    async def get_by_branch_id(self, branch_id: int) -> list[CategoryModel]:
        result = await self.session.execute(
            select(CategoryModel).where(CategoryModel.branch_id == branch_id)
        )
        return list(result.scalars().all())
    
    async def update(self, category: CategoryModel) -> CategoryModel:
        result = await self.session.execute(
            update(CategoryModel)
            .where(CategoryModel.id == category.id)
            .values(
                name=category.name,
                description=category.description,
                branch_id=category.branch_id,
                is_active=category.is_active,
            )
            .returning(CategoryModel)
        )
        obj = result.scalar_one()
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
    
    async def delete(self, category_id: int) -> CategoryModel:
        result = await self.session.execute(
            delete(CategoryModel)
            .where(CategoryModel.id == category_id)
        )
        await self.session.commit()
        return result.rowcount > 0

    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[CategoryModel]:
        query = select(CategoryModel)
        
        if filters:
            query = query.filter_by(**filters)
        
        result = await self.session.execute(
            query.order_by(CategoryModel.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())