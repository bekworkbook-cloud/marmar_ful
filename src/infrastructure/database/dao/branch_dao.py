from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.models.branch import Branch as BranchModel

class BranchDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, branch: BranchModel) -> BranchModel:
        self.session.add(instance=branch)
        await self.session.commit()
        await self.session.refresh(branch)
        return branch

    async def count_all(self) -> int:
        result = await self.session.execute(
            select(func.count(BranchModel.id))
        )
        return result.scalar() or 0
    
    async def get_by_id(self, branch_id: int) -> BranchModel | None:
        result = await self.session.execute(
            select(BranchModel).where(BranchModel.id == branch_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[BranchModel]:
        result = await self.session.execute(
            select(BranchModel)
        )
        return list(result.scalars().all())
    
    async def update(self, branch: BranchModel) -> BranchModel:
        result = await self.session.execute(
            update(BranchModel)
            .where(BranchModel.id == branch.id)
            .values(
                name=branch.name,
                branch_code=branch.branch_code,
                description=branch.description,
                address=branch.address,
                landmark=branch.landmark,
                latitude=branch.latitude,
                longitude=branch.longitude,
                delivery_price=branch.delivery_price,
                is_active=branch.is_active,
            )
            .returning(BranchModel)
        )
        obj = result.scalar_one()
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
    
    async def delete(self, branch_id: int) -> bool:
        result = await self.session.execute(
            delete(BranchModel)
            .where(BranchModel.id == branch_id)
        )
        await self.session.commit()
        return result.rowcount > 0

    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[BranchModel]:
        query = select(BranchModel)
        
        if filters:
            query = query.filter_by(**filters)
        
        result = await self.session.execute(
            query.order_by(BranchModel.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())