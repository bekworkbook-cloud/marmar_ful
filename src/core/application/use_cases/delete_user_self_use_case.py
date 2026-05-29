from src.core.domain.interfaces.user_repo import UserRepository
from src.core.application.use_cases.dtos.auth_dtos import TokenDataDTO
from src.core.application.use_cases.dtos.user_dtos import UserDTO



class DeleteUserSelfUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, token_data: TokenDataDTO) -> UserDTO:
        return await self.user_repo.delete(user_id=token_data.user_id)