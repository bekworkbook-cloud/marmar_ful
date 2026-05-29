from src.core.domain.interfaces.user_repo import UserRepository
from src.core.domain.entities.user import User
from src.core.application.use_cases.dtos.user_dtos import UserDTO, UserUpdateDTO
from src.core.application.exceptions.not_found_exception import NotFoundException


class PutUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, user_id: int, user_update: UserUpdateDTO) -> UserDTO:
        user_entity = await self.user_repo.get_by_id(user_id)
        if not user_entity:
            raise NotFoundException(f"User with id {user_id} not found")
        
        user_entity.update_base_info(
            first_name=user_update.first_name,
            username=user_update.username,
            phone_number=user_update.phone_number
        )

        user_entity.update_role(user_update.role)
        user_entity.update_branch_id(user_update.branch_id)

        updated_entity = await self.user_repo.update(user_entity)
        
        return UserDTO(
            id=updated_entity.id,
            username=updated_entity.username,
            telegram_id=updated_entity.telegram_id,
            first_name=updated_entity.first_name,
            phone_number=updated_entity.phone_number,
            role=updated_entity.role,
            branch_id=updated_entity.branch_id
        )