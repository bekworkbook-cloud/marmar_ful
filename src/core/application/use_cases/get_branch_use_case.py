from src.core.domain.interfaces.branch_repo import BranchRepository
from src.core.application.use_cases.dtos.branch_dtos import BranchDTO, BranchIdDTO



class GetBranchUseCase:
    def __init__(self, branch_repo: BranchRepository):
        self.branch_repo = branch_repo

    async def execute(self, branch_id_dto: BranchIdDTO) -> BranchDTO:
        branch_data = await self.branch_repo.get_by_id(branch_id=branch_id_dto.id)
        return BranchDTO(
            id=branch_data.id,
            name=branch_data.name,
            branch_code=branch_data.branch_code,
            description=branch_data.description,
            address=branch_data.address,
            landmark=branch_data.landmark,
            latitude=branch_data.latitude,
            longitude=branch_data.longitude,
            delivery_price=branch_data.delivery_price,
            is_active=branch_data.is_active,
        )
        