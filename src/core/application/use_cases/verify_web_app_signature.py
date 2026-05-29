from src.core.domain.interfaces.user_repo import UserRepository
from src.core.domain.services.auth_service import AuthService
from src.core.application.exceptions.auth import UnauthorizedError
from src.core.application.use_cases.dtos.auth_dtos import UserTelegramInitionDTO, TokenDTO

class VerifyWebAppSignatureUseCase:
    def __init__(self, user_repo: UserRepository, auth_service: AuthService):
        self.user_repo = user_repo
        self.auth_service = auth_service

    async def execute(self, user_telegram_inition_dto: UserTelegramInitionDTO) -> TokenDTO:
        user = await self.user_repo.get_by_telegram_id(telegram_id=user_telegram_inition_dto.user.telegram_id)

        if not user:
            raise UnauthorizedError("User by telegram_id not found")

        data = {
            "sub": str(user.id),
            "role": str(user.role.value)
        }
        token = self.auth_service.create_access_token(data=data)

        return TokenDTO(access_token=token, token_type="bearer")
