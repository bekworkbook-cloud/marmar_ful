from src.core.domain.interfaces.category_repo import CategoryRepository
from src.core.application.use_cases.dtos.category_dtos import CategoryDTO, CategoriesDTO

class GetCategoriesUseCase:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo
    
    async def execute(self) -> CategoriesDTO:
        categories_entities = await self.category_repo.get_all()
        categories_dtos_list = [
            CategoryDTO(
                id=category.id,
                name=category.name,
                description=category.description,
                branch_id=category.branch_id,
                is_active=category.is_active
            )
            for category in categories_entities
        ]
        return CategoriesDTO(categories=categories_dtos_list)
