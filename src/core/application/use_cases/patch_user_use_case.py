from src.core.domain.interfaces.user_repo import UserRepository
from src.core.application.use_cases.dtos.user_dtos import UserDTO, UserIdDTO, UserUpdateDTO

class PatchUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, user_id: UserIdDTO, user_update: UserUpdateDTO) -> UserDTO:
        user_entity = await self.user_repo.get_by_id(user_id=user_id.id)
        
        user_entity.update_fields(
            telegram_id=user_update.telegram_id,
            first_name=user_update.first_name,
            username=user_update.username,
            role=user_update.role,
            branch_id=user_update.branch_id
        )
        
        updated_entity = await self.user_repo.update(user_entity)
        
        return UserDTO(
            id=updated_entity.id,
            telegram_id=updated_entity.telegram_id,
            first_name=updated_entity.first_name,
            username=updated_entity.username,
            role=updated_entity.role,
            branch_id=updated_entity.branch_id
        )