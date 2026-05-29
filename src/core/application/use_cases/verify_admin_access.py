from src.core.domain.interfaces.user_repo import UserRepository
from src.core.domain.enums.roles import UserRole
from src.core.application.exceptions.auth import ForbiddenError
from src.core.application.use_cases.dtos.auth_dtos import UserTelegramDTO

class VerifyAdminAccessUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, user_telegram_dto: UserTelegramDTO):
        user = await self.user_repo.get_by_telegram_id(telegram_id=user_telegram_dto.telegram_id)
        
        if not user:
            raise ForbiddenError("Admin by id not found")
        
        if user.role != UserRole.ADMIN:
            raise ForbiddenError("Access denied")
