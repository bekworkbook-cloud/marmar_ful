from src.core.domain.interfaces.branch_repo import BranchRepository
from src.core.application.use_cases.dtos.branch_dtos import BranchDTO, BranchIdDTO, BranchUpdateDTO

class PutBranchUseCase:
    def __init__(self, branch_repo: BranchRepository):
        self.branch_repo = branch_repo

    async def execute(self, branch_id: BranchIdDTO, branch_update_dto: BranchUpdateDTO) -> BranchDTO:
        branch_entity = await self.branch_repo.get_by_id(branch_id=branch_id.id)
        
        branch_entity.update_fields(
            name=branch_update_dto.name,
            branch_code=branch_update_dto.branch_code,
            description=branch_update_dto.description,
            address=branch_update_dto.address,
            landmark=branch_update_dto.landmark,
            latitude=branch_update_dto.latitude,
            longitude=branch_update_dto.longitude,
            delivery_price=branch_update_dto.delivery_price,
            is_active=branch_update_dto.is_active
        )
        
        updated_entity = await self.branch_repo.update(branch_entity)
        
        return BranchDTO(
            id=updated_entity.id,
            name=updated_entity.name,
            branch_code=updated_entity.branch_code,
            description=updated_entity.description,
            address=updated_entity.address,
            landmark=updated_entity.landmark,
            latitude=updated_entity.latitude,
            longitude=updated_entity.longitude,
            delivery_price=updated_entity.delivery_price,
            is_active=updated_entity.is_active
        )