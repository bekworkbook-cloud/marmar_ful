from abc import ABC, abstractmethod
from src.core.domain.entities.order_item import OrderItem


class OrderItemRepository(ABC):

    @abstractmethod
    async def add(self, order_item: OrderItem) -> OrderItem:
        pass

    @abstractmethod
    async def get(self, order_item_id: int) -> OrderItem:
        pass

    @abstractmethod
    async def update(self, order_item: OrderItem) -> OrderItem:
        pass

    @abstractmethod
    async def delete(self, order_id: int):
        pass

    @abstractmethod
    async def list(self, limit: int = 10, offset: int = 0, **filters) -> list[OrderItem]:
        pass
