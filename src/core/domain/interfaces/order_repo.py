# from typing import List
from abc import ABC, abstractmethod

# from src.core.domain.entities.order import Order
# from src.core.domain.enums.order_status import OrderStatus

# class OrderRepository(ABC):

#     @abstractmethod
#     async def add(self, order: Order) -> Order:
#         """Создать новый заказ"""
#         pass

#     @abstractmethod
#     async def get_by_id(self, order_id: int) -> Order | None:
#         """Получить один заказ"""
#         pass

#     @abstractmethod
#     async def update(self, order: Order) -> Order:
#         """Обновить заказ целиком"""
#         pass

#     @abstractmethod
#     async def delete(self, order_id: int) -> None:
#         """Удалить заказ"""
#         pass

#     @abstractmethod
#     async def list(self, limit: int = 10, offset: int = 0, **filters) -> list[Order]:
#         """
#         Универсальный поиск. 
#         Сюда можно передать customer_id, courier_id или status.
#         """
#         pass


# core/domain/interfaces/order_repo.py

class OrderRepository(ABC):
    @abstractmethod
    async def count_active(self) -> int:
        pass

    @abstractmethod
    async def revenue_today(self) -> float:
        pass