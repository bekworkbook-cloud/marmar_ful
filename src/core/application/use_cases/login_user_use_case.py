from src.core.domain.interfaces.user_repo import UserRepository
from src.core.domain.services.auth_service import AuthService
from src.core.application.exceptions.auth import UnauthorizedError
from src.core.application.use_cases.dtos.auth_dtos import UserLoginDTO, TokenDTO

class LogInUserUseCase:
    def __init__(self, user_repo: UserRepository, auth_service: AuthService):
        self.user_repo = user_repo
        self.auth_service = auth_service

    async def execute(self, user_login_dto: UserLoginDTO) -> TokenDTO:
        user = await self.user_repo.get_by_username(username=user_login_dto.username)
        
        if not user or not self.auth_service.verify_password(plain_password=user_login_dto.password, hashed_password=user.hashed_pwd):
            raise UnauthorizedError("Wrong login or password")
        
        data = {
            "sub": str(user.id),
            "role": str(user.role.value)
        }
        token = self.auth_service.create_access_token(data=data)
        return TokenDTO(access_token=token, token_type="bearer")