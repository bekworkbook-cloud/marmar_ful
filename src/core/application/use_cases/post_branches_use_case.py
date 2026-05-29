from src.core.domain.interfaces.branch_repo import BranchRepository
from src.core.domain.entities.branch import Branch
from src.core.application.use_cases.dtos.branch_dtos import BranchDTO, BranchCreateDTO

class PostBranchesUseCase:
    def __init__(self, branch_repo: BranchRepository):
        self.branch_repo = branch_repo

    async def execute(self, branch_create_dto: BranchCreateDTO) -> BranchDTO:
        branch_entity = Branch(
            id=None,
            name=branch_create_dto.name,
            branch_code=branch_create_dto.branch_code,
            description=branch_create_dto.description,
            address=branch_create_dto.address,
            landmark=branch_create_dto.landmark,
            latitude=branch_create_dto.latitude,
            longitude=branch_create_dto.longitude,
            delivery_price=branch_create_dto.delivery_price,
            is_active=branch_create_dto.is_active,
        )
        
        created_entity = await self.branch_repo.add(branch=branch_entity)
        
        return BranchDTO(
            id=created_entity.id,
            name=created_entity.name,
            branch_code=created_entity.branch_code,
            description=created_entity.description,
            address=created_entity.address,
            landmark=created_entity.landmark,
            latitude=created_entity.latitude,
            longitude=created_entity.longitude,
            delivery_price=created_entity.delivery_price,
            is_active=created_entity.is_active,
        )