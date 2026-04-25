from abc import ABC, abstractmethod

from src.core.domain.entities.product import Product


class ProductRepository(ABC):
    @abstractmethod
    async def get_by_id(self, product_id: int) -> Product | None:
        pass

    @abstractmethod
    async def list(self, limit: int = 10, offset: int = 0, **filters) -> list[Product]:
        """
        Универсальный метод. Заменяет все 'get_by_category', 'get_active' и т.д.
        Пример использования: 
        repo.list(category_id=5, is_active=True, limit=20)
        """
        pass

    @abstractmethod
    async def update(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def add(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def delete(self, product_id: int) -> None:
        pass