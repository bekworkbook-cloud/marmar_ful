from src.core.domain.interfaces.category_repo import CategoryRepository
from src.core.domain.entities.category import Category
from src.infrastructure.database.models.category import Category as CategoryModel
from src.infrastructure.database.dao.category_dao import CategoryDAO

class CategoryRepositoryImpl(CategoryRepository):
    def __init__(self, category_dao: CategoryDAO):
        self.category_dao = category_dao

    def _to_entity(self, model: CategoryModel) -> Category:
        return Category(
            id=model.id,
            name=model.name,
            description=model.description,
            branch_id=model.branch_id,
            is_active=model.is_active
        )

    def _to_model(self, entity: Category) -> CategoryModel:
        return CategoryModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            branch_id=entity.branch_id,
            is_active=entity.is_active
        )

    async def add(self, category: Category) -> Category:
        category_model = self._to_model(category)
        created_model = await self.category_dao.add(category_model)
        return self._to_entity(created_model) 

    async def get_by_id(self, category_id: int) -> Category:
        model = await self.category_dao.get_by_id(category_id)
        return self._to_entity(model)

    async def get_all(self) -> list[Category]:
        models = await self.category_dao.get_all()
        return [self._to_entity(model) for model in models]

    async def get_by_branch_id(self, branch_id: int) -> list[Category]:
        models = await self.category_dao.get_by_branch_id(branch_id)
        return [self._to_entity(model) for model in models]

    async def update(self, category: Category) -> Category:
        category_model = self._to_model(category)
        updated_model = await self.category_dao.update(category_model)
        return self._to_entity(updated_model)

    async def delete(self, category_id: int) -> None:
        return await self.category_dao.delete(category_id)

    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[Category]:
        models = await self.category_dao.get_list(limit=limit, offset=offset, **filters)
        return [self._to_entity(model) for model in models]