from src.core.domain.interfaces.user_repo import UserRepository
from src.core.application.use_cases.dtos.user_dtos import GetUsersDTO, GetUserDTO, GetUsersInputDTO

class GetUsersUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, get_users_input_dto: GetUsersInputDTO) -> GetUsersDTO:
        role = get_users_input_dto.role
        branch_id = get_users_input_dto.branch_id
        limit = get_users_input_dto.limit
        offset = get_users_input_dto.offset
        
        user_entities = await self.user_repo.get_list(
            role=role,
            branch_id=branch_id,
            limit=limit,
            offset=offset
        )
        print(user_entities)
        
        users_dto_list = [
            GetUserDTO(
                id=user.id,
                telegram_id=user.telegram_id,
                first_name=user.first_name,
                username=user.username,
                role=user.role,
                branch_id=user.branch_id
            )
            for user in user_entities
        ]
        print(users_dto_list)
        return GetUsersDTO(items=users_dto_list)
        