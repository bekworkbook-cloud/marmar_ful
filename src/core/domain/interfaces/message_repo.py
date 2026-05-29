from abc import ABC, abstractmethod
from src.core.domain.entities.message import Message


class MessageRepository(ABC):
    @abstractmethod
    async def post_message(self, message: Message) -> Message:
        pass
    
    # @abstractmethod
    # async def get_by_order(self, order_id: int) -> list[Message]:
        # pass

    @abstractmethod
    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[Message]:
        pass

    @abstractmethod
    async def add(self, message: Message) -> Message:
        pass

    @abstractmethod
    async def get_messages(self, order_id: int) -> list[Message]:
        pass

    @abstractmethod
    async def post_message(self, message: Message) -> Message:
        pass

    
