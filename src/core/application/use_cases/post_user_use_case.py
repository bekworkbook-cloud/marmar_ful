from src.core.domain.interfaces.user_repo import UserRepository
from src.core.domain.entities.user import User
from src.core.application.use_cases.dtos.user_dtos import UserDTO, UserCreateDTO
from src.core.domain.services.auth_service import AuthService
from src.core.domain.enums.roles import UserRole

class PostUserUseCase:
    def __init__(self, user_repo: UserRepository, auth_service: AuthService):
        self.user_repo = user_repo
        self.auth_service = auth_service
    
    async def execute(self, user_create: UserCreateDTO) -> UserDTO:
        hashed_pwd = self.auth_service.get_password_hash(password=user_create.password)
        user_entity = User(
            id=None,
            telegram_id=None,
            phone_number=None,
            first_name=None,
            username=user_create.username,
            hashed_pwd=hashed_pwd,
            role=UserRole(user_create.role),
            branch_id=user_create.branch_id,
            permissions=None
        )
        
        created_entity = await self.user_repo.add(user=user_entity)
        
        return UserDTO(
            id=created_entity.id,
            telegram_id=created_entity.telegram_id,
            first_name=created_entity.first_name,
            username=created_entity.username,
            role=created_entity.role,
            branch_id=created_entity.branch_id
        )