from src.core.domain.interfaces.user_repo import UserRepository
from src.core.domain.entities.user import User
from src.infrastructure.database.models.user import User as UserModel
from src.infrastructure.database.dao.user_dao import UserDAO
from src.core.domain.enums.roles import UserRole
from src.core.domain.services.access_control import ROLE_PERMISSIONS
from src.infrastructure.database.exceptions.auth_error import AuthenticationError

class UserRepositoryImpl(UserRepository):
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    def _to_entity(self, model: UserModel) -> User:
        actual_role = UserRole(model.role)
        return User(
            id=model.id,
            telegram_id=model.telegram_id,
            phone_number=model.phone_number,
            first_name=model.first_name,
            username=model.username,
            hashed_pwd=model.hashed_pwd,
            role=actual_role,
            branch_id=model.branch_id,
            permissions=ROLE_PERMISSIONS.get(actual_role, [])
        )

    def _to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            telegram_id=entity.telegram_id,
            first_name=entity.first_name,
            username=entity.username,
            hashed_pwd=entity.hashed_pwd,
            role=entity.role.value if isinstance(entity.role, UserRole) else entity.role,
            branch_id=entity.branch_id
        )

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        model = await self.user_dao.get_by_telegram_id(telegram_id)    
        if not model:
            return None
        return self._to_entity(model)

    async def get_by_id(self, user_id: int) -> User:
        model = await self.user_dao.get_by_id(user_id)
        if model is None:
            raise AuthenticationError("User by id not found")
        return self._to_entity(model)
    
    async def get_by_username(self, username: str) -> User | None:
        model = await self.user_dao.get_by_username(username)
        if not model:
            return None
        return self._to_entity(model)
    
    async def count_all(self) -> int:
        return await self.user_dao.count_all()
    
    async def add(self, user: User) -> User:
        model = self._to_model(user)
        created_model = await self.user_dao.add(model)
        return self._to_entity(created_model)
    
    async def update(self, user: User) -> User:
        model = self._to_model(user)
        updated_model = await self.user_dao.update(model)
        return self._to_entity(updated_model)
    
    async def delete(self, user_id: int) -> None:
        return await self.user_dao.delete(user_id)

    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[User]:
        models = await self.user_dao.get_list(limit=limit, offset=offset, **filters)
        return [self._to_entity(model) for model in models]