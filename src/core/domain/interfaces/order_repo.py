from abc import ABC, abstractmethod

from src.core.domain.entities.order import Order


class OrderRepository(ABC):
    @abstractmethod
    async def get_by_id(self, order_id: int) -> Order:
        pass

    @abstractmethod
    async def add(self, order: Order) -> Order:
        pass

    @abstractmethod
    async def update(self, order: Order) -> Order:
        pass

    @abstractmethod
    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[Order]:
        pass

