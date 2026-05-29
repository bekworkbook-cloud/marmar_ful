from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.models.order_item import OrderItem as OrderItemModel

class OrderItemDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, order_item: OrderItemModel) -> OrderItemModel:
        self.session.add(instance=order_item)
        await self.session.commit()
        await self.session.refresh(order_item)
        return order_item

    async def get_by_id(self, order_item_id: int) -> OrderItemModel | None:
        result = await self.session.execute(
            select(OrderItemModel).where(OrderItemModel.id == order_item_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_order_id(self, order_id: int) -> list[OrderItemModel]:
        result = await self.session.execute(
            select(OrderItemModel).where(OrderItemModel.order_id == order_id)
        )
        return list(result.scalars().all())
    
    async def update(self, order_item: OrderItemModel) -> OrderItemModel:
        result = await self.session.execute(
            update(OrderItemModel)
            .where(OrderItemModel.id == order_item.id)
            .values(
                order_id=order_item.order_id,
                product_id=order_item.product_id,
                quantity=order_item.quantity,
                price=order_item.price,
            )
            .returning(OrderItemModel)
        )
        obj = result.scalar_one()
        await self.session.commit()
        return obj
    
    async def delete(self, order_item_id: int) -> OrderItemModel:
        result = await self.session.execute(
            delete(OrderItemModel)
            .where(OrderItemModel.id == order_item_id)
            .returning(OrderItemModel)
        )
        obj = result.scalar_one()
        await self.session.commit()
        return obj
    
    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[OrderItemModel]:
        query = select(OrderItemModel)
        
        if filters:
            query = query.filter_by(**filters)
        
        result = await self.session.execute(
            query.order_by(OrderItemModel.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())