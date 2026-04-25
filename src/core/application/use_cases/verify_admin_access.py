from src.core.domain.enums.permissions import Permission
from src.core.domain.exceptions.access import DomainAccessDeniedError

class VerifyAdminAccessUseCase:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    async def execute(self, telegram_id: int) -> None:
        user = await self.user_repo.get_by_telegram_id(telegram_id=telegram_id)

        if not user:
            raise DomainAccessDeniedError("User not found in system")
        
        user.require_permission(Permission.ACCESS_ADMIN_CHAT)
