from src.core.domain.interfaces.user_repo import UserRepository
from src.core.application.use_cases.dtos.auth_dtos import TokenDataDTO
from src.core.application.use_cases.dtos.user_dtos import UserDTO
from src.core.application.exceptions.auth import UnauthorizedError

class GetMeUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    async def execute(self, token_dto: TokenDataDTO) -> UserDTO:
        user = await self.user_repo.get_by_id(user_id=token_dto.user_id)
        
        print(user.role)
        print(token_dto.user_role)

        if str(user.role.value) != str(token_dto.user_role):
            raise UnauthorizedError("Token role mismatch with database")
        
        return UserDTO(
            id=user.id,
            telegram_id=user.telegram_id,
            phone_number=user.phone_number,
            first_name=user.first_name,
            username=user.username,
            role=user.role,
            branch_id=user.branch_id
        )
