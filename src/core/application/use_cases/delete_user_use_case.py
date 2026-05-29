from src.core.domain.interfaces.user_repo import UserRepository
from src.core.application.use_cases.dtos.user_dtos import DeleteUserDTO


class DeleteUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, delete_user_dto: DeleteUserDTO) -> bool:
        return await self.user_repo.delete(user_id=delete_user_dto.user_id)

       