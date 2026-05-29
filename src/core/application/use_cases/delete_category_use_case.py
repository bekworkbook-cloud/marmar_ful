from src.core.domain.interfaces.category_repo import CategoryRepository
from src.core.application.use_cases.dtos.category_dtos import CategoryDTO, CategoryIdDTO

class DeleteCategoryUseCase:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    async def execute(self, category_id: CategoryIdDTO) -> bool:
        return await self.category_repo.delete(category_id=category_id.id)
        