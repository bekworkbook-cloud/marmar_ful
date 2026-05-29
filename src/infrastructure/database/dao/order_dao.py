from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.models.order import Order as OrderModel

class OrderDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, order_id: int) -> OrderModel | None:
        result = await self.session.execute(
            select(OrderModel).where(OrderModel.id == order_id)
        )
        return result.scalar_one_or_none()

    async def add(self, order: OrderModel) -> OrderModel:
        self.session.add(instance=order)
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def update(self, order: OrderModel) -> OrderModel:
        result = await self.session.execute(
            update(OrderModel)
            .where(OrderModel.id == order.id)
            .values(
                customer_id=order.customer_id,
                operator_id=order.operator_id,
                courier_id=order.courier_id,
                branch_id=order.branch_id,
                status=order.status,
                payment_method=order.payment_method,
                total_price=order.total_price,
                is_accepted=order.is_accepted,
                address=order.address,
                landmark=order.landmark,
                latitude=order.latitude,
                longitude=order.longitude,
            )
            .returning(OrderModel)
        )
        obj = result.scalar_one()
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
    
    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[OrderModel]:
        query = select(OrderModel)
        
        if filters:
            query = query.filter_by(**filters)
        
        result = await self.session.execute(
            query.order_by(OrderModel.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
