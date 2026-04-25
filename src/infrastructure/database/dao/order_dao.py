from sqlalchemy import select, func

from src.infrastructure.database.models.order import Order as OrderModel
from src.shared.utils.datetime import today_start


class OrderDAO:

    def __init__(self, session):
        self.session = session

    async def count_active(self):
        result = await self.session.execute(
            select(func.count(OrderModel.id))
            .where(OrderModel.status == "active")
        )
        return result.scalar()

    async def revenue_today(self):
        result = await self.session.execute(
            select(func.sum(OrderModel.total_price))
            .where(OrderModel.created_at >= today_start())
        )
        return result.scalar() or 0
