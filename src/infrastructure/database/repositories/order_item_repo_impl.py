from src.core.domain.interfaces.order_item_repo import OrderItemRepository
from src.core.domain.entities.order_item import OrderItem
from src.infrastructure.database.models.order_item import OrderItem as OrderItemModel
from src.infrastructure.database.dao.order_item_dao import OrderItemDAO

class OrderItemRepositoryImpl(OrderItemRepository):
    def __init__(self, order_item_dao: OrderItemDAO):
        self.order_item_dao = order_item_dao

    def _to_entity(self, model: OrderItemModel) -> OrderItem:
        return OrderItem(
            id=model.id,
            order_id=model.order_id,
            product_id=model.product_id,
            quantity=model.quantity,
            price=model.price
        )

    def _to_model(self, entity: OrderItem) -> OrderItemModel:
        return OrderItemModel(
            id=entity.id,
            order_id=entity.order_id,
            product_id=entity.product_id,
            quantity=entity.quantity,
            price=entity.price
        )

    async def add(self, order_item: OrderItem) -> OrderItem:
        model = self._to_model(order_item)
        created_model = await self.order_item_dao.add(model)
        return self._to_entity(created_model)

    async def get_by_id(self, order_item_id: int) -> OrderItem:
        model = await self.order_item_dao.get_by_id(order_item_id)
        return self._to_entity(model)
    
    async def get_by_order_id(self, order_id: int) -> list[OrderItem]:
        models = await self.order_item_dao.get_by_order_id(order_id)
        return [self._to_entity(model) for model in models]
    
    async def update(self, order_item: OrderItem) -> OrderItem:
        model = self._to_model(order_item)
        updated_model = await self.order_item_dao.update(model)
        return self._to_entity(updated_model)
    
    async def delete(self, order_item_id: int) -> None:
        await self.order_item_dao.delete(order_item_id)

    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[OrderItem]:
        models = await self.order_item_dao.get_list(limit=limit, offset=offset, **filters)
        return [self._to_entity(model) for model in models]