from src.core.domain.entities.user import User
from src.core.domain.enums.roles import UserRole
from src.core.domain.services.access_control import ROLE_PERMISSIONS

class UserRepositoryImpl:
    def __init__(self, dao):
        self.dao = dao

    async def get_by_id(self, user_id: int) -> User | None:
        model = await self.dao.get_by_id(user_id)
        if not model:
            return None
        return self._map_to_domain(model)
    
    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        model = await self.dao.get_by_telegram_id(telegram_id)
        if not model:
            return None
        return self._map_to_domain(model)

    async def count_all(self) -> int:
        # Обязательно await, чтобы не вернуть корутину в UseCase
        return await self.dao.count_all()

    def _map_to_domain(self, model) -> User:
        try:
            # Если в базе строка 'ADMIN', преобразуем в UserRole.ADMIN
            role_enum = UserRole(model.role)
        except (ValueError, TypeError):
            role_enum = UserRole.GUEST

        # Теперь role_enum — это элемент Enum (хешируемый), а не dict или str
        permissions = ROLE_PERMISSIONS.get(role_enum, set())

        return User(
            id=model.id,
            telegram_id=model.telegram_id,
            first_name=model.first_name,
            username=model.username,
            role=role_enum,      # ПЕРЕДАЕМ ОБЪЕКТ ENUM
            branch_id=model.branch_id, # ПЕРЕДАЕМ ID (INT), А НЕ ОБЪЕКТ MODEL
            permissions=permissions
        )