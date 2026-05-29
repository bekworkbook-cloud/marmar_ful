from src.core.domain.interfaces.user_repo import UserRepository
from src.core.domain.services.auth_service import AuthService
from src.core.domain.entities.user import User
from src.core.application.use_cases.dtos.auth_dtos import UserRegisterDTO, TokenDTO
from src.core.domain.enums.roles import UserRole

class RegisterUserUseCase:
    def __init__(self, user_repo: UserRepository, auth_service: AuthService):
        self.user_repo = user_repo
        self.auth_service = auth_service

    async def execute(self, user_register: UserRegisterDTO) -> TokenDTO:
        hashed_password = self.auth_service.get_password_hash(password=user_register.password)
        
        user_entity = User(
            id=None,
            telegram_id=None,
            first_name=None,
            phone_number=None,
            username=user_register.username,
            hashed_pwd=hashed_password,
            role=UserRole.CUSTOMER,
            branch_id=None,
            permissions=[]
        )
        
        created_entity = await self.user_repo.add(user=user_entity)
        
        data = {
            "sub": str(created_entity.id),
            "role": str(created_entity.role.value)
        }
        token = self.auth_service.create_access_token(data=data)
        
        return TokenDTO(access_token=token, token_type="bearer")