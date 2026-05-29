from abc import ABC, abstractmethod
from src.core.domain.entities.category import Category


class CategoryRepository(ABC):

    @abstractmethod
    async def add(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def get_all(self) -> list[Category]:
        pass


    @abstractmethod
    async def get_by_id(self, category_id: int) -> Category:
        pass

    @abstractmethod
    async def get_by_branch_id(self, branch_id: int) -> list[Category]:    
        pass

    @abstractmethod
    async def update(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def delete(self, category_id: int) -> Category:
        pass

    @abstractmethod
    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[Category]:
        pass
