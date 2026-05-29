

from abc import ABC, abstractmethod
from src.core.domain.entities.payment import PaymentLog

class PaymentLogRepository(ABC):
    @abstractmethod
    async def get_by_id(self, payment_log_id: int) -> PaymentLog:
        pass

    @abstractmethod
    async def get_by_order_id(self, order_id: int, branch_id: int, courier_id: int, limit: int = 10, offset: int = 0) -> list[PaymentLog]:
        pass

    @abstractmethod
    async def update(self, payment_log: PaymentLog) -> PaymentLog:
        pass

    @abstractmethod
    async def delete(self, payment_log_id: int) -> PaymentLog:
        pass

    @abstractmethod
    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[PaymentLog]:
        pass