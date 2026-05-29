from src.core.domain.interfaces.user_repo import UserRepository
from src.core.domain.enums.roles import UserRole
from src.core.application.exceptions.auth import ForbiddenError
from src.core.application.use_cases.dtos.auth_dtos import UserTelegramDTO

class VerifyOperatorAccessUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, user_telegram: UserTelegramDTO) -> None:
        user = await self.user_repo.get_by_telegram_id(telegram_id=user_telegram.telegram_id)

        if not user:
            raise ForbiddenError("Operator by id not found")

        if user.role not in (UserRole.OPERATOR, UserRole.MAINOPERATOR):
            raise ForbiddenError("Access denied")
