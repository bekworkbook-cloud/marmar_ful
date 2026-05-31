from src.core.domain.interfaces.category_repo import CategoryRepository
from src.core.application.use_cases.dtos.category_dtos import CategoryDTO, CategoriesDTO, GetCategoryInputDTO
from src.core.application.use_cases.dtos.branch_dtos import BranchIdDTO

class GetCategoriesByBranchIdUseCase:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo
    
    async def execute(self, get_category_input_dto: GetCategoryInputDTO) -> CategoriesDTO:
        branch_id = get_category_input_dto.branch_id
        limit = get_category_input_dto.limit
        offset = get_category_input_dto.offset
        categories_entities = await self.category_repo.get_list(branch_id=branch_id, limit=limit, offset=offset)
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
        return CategoriesDTO(items=categories_dtos_list)