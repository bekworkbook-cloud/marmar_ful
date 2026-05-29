from src.core.domain.interfaces.category_repo import CategoryRepository
from src.core.application.use_cases.dtos.category_dtos import CategoryDTO, CategoryIdDTO

class GetCategoryUseCase:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    async def execute(self, category_id: CategoryIdDTO) -> CategoryDTO:
        category = await self.category_repo.get_by_id(category_id=category_id.id)
        return CategoryDTO(
            id=category.id,
            name=category.name,
            description=category.description,
            branch_id=category.branch_id,
            is_active=category.is_active
        )