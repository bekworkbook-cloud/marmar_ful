from src.core.domain.interfaces.user_repo import UserRepository
from src.core.domain.enums.roles import UserRole
from src.core.application.exceptions.auth import ForbiddenError
from src.core.application.use_cases.dtos.auth_dtos import UserTelegramDTO

class VerifyCourierAccessUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    async def execute(self, user_telegram_dto: UserTelegramDTO) -> None:
        print(user_telegram_dto.telegram_id)
        user = await self.user_repo.get_by_telegram_id(telegram_id=user_telegram_dto.telegram_id)
        print(user)
        if not user:
            raise ForbiddenError("Courier by id not found")
        
        if user.role != UserRole.COURIER:
            raise ForbiddenError("Access denied")
    