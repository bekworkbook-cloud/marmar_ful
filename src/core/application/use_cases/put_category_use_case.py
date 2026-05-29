from src.core.domain.interfaces.category_repo import CategoryRepository
from src.core.application.use_cases.dtos.category_dtos import CategoryDTO, CategoryIdDTO, CategoryUpdateDTO


class PutCategoryUseCase:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo
    
    async def execute(self, category_id: CategoryIdDTO, category_update: CategoryUpdateDTO) -> CategoryDTO:
        category_entity = await self.category_repo.get_by_id(category_id=category_id.id)
        
        category_entity.update_fields(
            name=category_update.name,
            description=category_update.description,
            branch_id=category_update.branch_id,
            is_active=category_update.is_active
        )

        updated_entity = await self.category_repo.update(category_entity)
        
        return CategoryDTO(
            id=updated_entity.id,
            name=updated_entity.name,
            description=updated_entity.description,
            branch_id=updated_entity.branch_id,
            is_active=updated_entity.is_active
        )