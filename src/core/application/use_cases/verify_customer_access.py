from src.core.domain.interfaces.user_repo import UserRepository
from src.core.domain.entities.user import User
from src.core.domain.enums.roles import UserRole
from src.core.application.use_cases.dtos.auth_dtos import UserTelegramDTO

class VerifyCustomerAccessUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, user_telegram_dto: UserTelegramDTO) -> None:
        user = await self.user_repo.get_by_telegram_id(telegram_id=user_telegram_dto.telegram_id)
        
        if not user:
            user_entity = User(
                id=None,
                telegram_id=user_telegram_dto.telegram_id,
                phone_number=None,
                first_name=None,
                username=user_telegram_dto.username,
                hashed_pwd=None,
                role=UserRole.CUSTOMER,
                branch_id=None,
                permissions=None,
            )
            await self.user_repo.add(user=user_entity)
