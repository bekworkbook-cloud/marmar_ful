from src.core.domain.enums.roles import UserRole
from src.core.domain.enums.permissions import Permission
from src.core.domain.exceptions.access import DomainAccessDeniedError

class User:
    def __init__(
        self,
        id: int | None,
        telegram_id: int,
        first_name: str,
        username: str | None,
        role: UserRole,
        branch_id: int | None,
        permissions: set[Permission]
    ):
        if not isinstance(role, UserRole):
            raise TypeError("role must be UserRole")

        self.id = id
        self.telegram_id = telegram_id
        self.first_name = first_name
        self.username = username
        self.role = role
        self.branch_id = branch_id
        self.permissions = permissions

    def has_permission(self, permission: Permission) -> bool:
        return permission in self.permissions
    
    def require_permission(self, permission: Permission) -> None:
        if not self.has_permission(permission):
            raise DomainAccessDeniedError("Forbidden: insufficient permissions")