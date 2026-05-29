from src.core.domain.interfaces.user_repo import UserRepository
from src.core.application.use_cases.dtos.user_dtos import UserDTO, GetUserInputDTO

class GetUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, get_user_input_dto: GetUserInputDTO) -> UserDTO:
        user_id = get_user_input_dto.user_id
        user = await self.user_repo.get_by_id(user_id=user_id)
        return UserDTO(
            id=user.id,
            telegram_id=user.telegram_id,
            username=user.username,
            phone_number=user.phone_number,
            first_name=user.first_name,
            role=user.role,
            branch_id=user.branch_id
        )