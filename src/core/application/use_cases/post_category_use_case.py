from src.core.domain.interfaces.category_repo import CategoryRepository
from src.core.domain.entities.category import Category
from src.core.application.use_cases.dtos.category_dtos import CategoryDTO, CategoryCreateDTO

class PostCategoryUseCase:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    async def execute(self, category_create: CategoryCreateDTO) -> CategoryDTO:
        category_entity = Category(
            id=None,
            name=category_create.name,
            description=category_create.description,
            branch_id=category_create.branch_id,
            is_active=category_create.is_active
        )
        
        created_entity = await self.category_repo.add(category=category_entity)
        
        return CategoryDTO(
            id=created_entity.id,
            name=created_entity.name,
            description=created_entity.description,
            branch_id=created_entity.branch_id,
            is_active=created_entity.is_active
        )