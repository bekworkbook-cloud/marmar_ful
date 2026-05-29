from abc import ABC, abstractmethod

from src.core.domain.entities.branch import Branch


class BranchRepository(ABC):
    
    @abstractmethod
    async def add(self, branch: int) -> Branch:
        pass
    
    @abstractmethod
    async def get_by_id(self, branch_id: int) -> Branch:
        pass

    @abstractmethod
    async def get_all(self) -> list[Branch]:
        pass

    @abstractmethod
    async def update(self, branch_entity: Branch) -> Branch:
        pass

    @abstractmethod
    async def delete(self, branch_id: int) -> Branch:
        pass

    @abstractmethod
    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[Branch]:
        pass
    