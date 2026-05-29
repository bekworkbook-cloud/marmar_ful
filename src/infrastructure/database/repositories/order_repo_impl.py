from src.core.domain.interfaces.order_repo import OrderRepository
from src.core.domain.entities.order import Order
from src.infrastructure.database.models.order import Order as OrderModel
from src.infrastructure.database.dao.order_dao import OrderDAO

class OrderRepositoryImpl(OrderRepository):
    def __init__(self, order_dao: OrderDAO):
        self.order_dao = order_dao

    def _to_entity(self, model: OrderModel) -> Order:
        return Order(
            id=model.id,
            customer_id=model.customer_id,
            operator_id=model.operator_id,
            courier_id=model.courier_id,
            branch_id=model.branch_id,
            status=model.status,
            payment_method=model.payment_method,
            total_price=model.total_price,
            is_accepted=model.is_accepted,
            address=model.address,
            landmark=model.landmark,
            latitude=model.latitude,
            longitude=model.longitude
        )

    def _to_model(self, entity: Order) -> OrderModel:
        return OrderModel(
            id=entity.id,
            customer_id=entity.customer_id,
            operator_id=entity.operator_id,
            courier_id=entity.courier_id,
            branch_id=entity.branch_id,
            status=entity.status,
            payment_method=entity.payment_method,
            total_price=entity.total_price,
            is_accepted=entity.is_accepted,
            address=entity.address,
            landmark=entity.landmark,
            latitude=entity.latitude,
            longitude=entity.longitude
        )

    async def add(self, order: Order) -> Order:
        order_model = self._to_model(order)
        created_model = await self.order_dao.add(order_model)
        return self._to_entity(created_model)

    async def get_by_id(self, order_id: int) -> Order:
        model = await self.order_dao.get_by_id(order_id)
        if not model:
            return None
        return self._to_entity(model)

    async def update(self, order: Order) -> Order:
        order_model = self._to_model(order)
        updated_model = await self.order_dao.update(order_model)
        return self._to_entity(updated_model)

    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[Order]:
        models = await self.order_dao.get_list(limit=limit, offset=offset, **filters)
        if not models:
            return []
        return [self._to_entity(model) for model in models]