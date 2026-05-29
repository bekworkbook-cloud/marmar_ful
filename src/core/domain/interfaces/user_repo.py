from abc import ABC, abstractmethod

from src.core.domain.entities.user import User


class UserRepository(ABC):

    @abstractmethod
    async def add(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> User:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> User:
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete(self, user_id: User) -> User:
        pass

    @abstractmethod
    async def count_all(self) -> int:
        pass

    @abstractmethod
    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[User]:
        pass
