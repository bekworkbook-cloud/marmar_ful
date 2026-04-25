from src.core.domain.interfaces.order_repo import OrderRepository



class OrderRepositoryImpl(OrderRepository):

    def __init__(self, dao):
        self.dao = dao

    async def count_active(self):
        return await self.dao.count_active()

    async def revenue_today(self):
        return await self.dao.revenue_today()