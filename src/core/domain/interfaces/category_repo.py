from abc import ABC, abstractmethod
from typing import List
from src.core.domain.entities.category import Category


class CategoryRepository(ABC):

    @abstractmethod
    async def add(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def get_by_id(self, category_id: int) -> list["Category"]:
        pass

    @abstractmethod
    async def update(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def delete(self, category_id: int) -> None:
        pass

    @abstractmethod
    async def list(self, limit: int = 10, offset: int = 0, **filters) -> list[Category]:
        pass
