from src.core.domain.interfaces.branch_repo import BranchRepository
from src.core.application.use_cases.dtos.branch_dtos import BranchesDTO, BranchDTO

class GetBranchesUseCase:
    def __init__(self, branch_repo: BranchRepository):
        self.branch_repo = branch_repo
    
    async def execute(self) -> BranchesDTO:
        branches_entities = await self.branch_repo.get_all()
        branches_dtos_list = [
            BranchDTO(
                id=branch.id,
                name=branch.name,
                branch_code=branch.branch_code,
                description=branch.description,
                address=branch.address,
                landmark=branch.landmark,
                latitude=branch.latitude,
                longitude=branch.longitude,
                delivery_price=branch.delivery_price,
                is_active=branch.is_active
            )
            for branch in branches_entities
        ]
        return BranchesDTO(items=branches_dtos_list)
    