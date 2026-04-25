from abc import ABC, abstractmethod

from src.core.domain.entities.branch import Branch


class BrachRepository(ABC):
    
    @abstractmethod
    async def add(self, branch: int) -> Branch:
        pass
    
    @abstractmethod
    async def get_by_id(self, branch_id: int) -> Branch:
        pass

    @abstractmethod

    @abstractmethod
    async def update(self, branch: Branch) -> Branch:
        pass

    @abstractmethod
    async def delete(self, branch_id: int):
        pass

    @abstractmethod
    async def list(self, limit: int = 10, offset: int = 0, **filters) -> list[Branch]:
        pass