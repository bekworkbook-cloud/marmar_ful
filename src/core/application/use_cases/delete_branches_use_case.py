from src.core.domain.interfaces.branch_repo import BranchRepository
from src.core.application.use_cases.dtos.branch_dtos import BranchDTO, DeleteBranchDTO

class DeleteBranchUseCase:
    def __init__(self, branch_repo: BranchRepository):
        self.branch_repo = branch_repo

    async def execute(self, delete_branch_dto: DeleteBranchDTO) -> bool:
        is_deleted = await self.branch_repo.delete(branch_id=delete_branch_dto.id)
        return is_deleted