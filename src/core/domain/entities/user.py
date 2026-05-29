from src.core.domain.enums.roles import UserRole
from src.core.domain.enums.permissions import Permission
from src.core.domain.exceptions.access import DomainAccessDeniedError

class User:
    def __init__(
        self,
        id: int | None,
        telegram_id: int | None,
        phone_number: str | None,
        first_name: str | None,
        username: str | None,
        hashed_pwd: str | None,
        role: UserRole,
        branch_id: int | None,
        permissions: set[Permission]
    ):
        if not isinstance(role, UserRole):
            raise TypeError("role must be UserRole")

        self.id = id
        self.telegram_id = telegram_id
        self.phone_number = phone_number
        self.first_name = first_name
        self.username = username
        self.hashed_pwd = hashed_pwd
        self.role = role
        self.branch_id = branch_id
        self.permissions = permissions

    def has_permission(self, permission: Permission) -> bool:
        return permission in self.permissions
    
    def require_permission(self, permission: Permission) -> None:
        if not self.has_permission(permission):
            raise DomainAccessDeniedError("Forbidden: insufficient permissions")
        

    def update_base_info(self, first_name: str, username: str, phone_number: str) -> None:
        self.first_name = first_name
        self.username = username
        self.phone_number = phone_number
    
    def update_hashed_pwd(self, hashed_pwd: str) -> None:
        self.hashed_pwd = hashed_pwd

    def update_role(self, role: UserRole) -> None:
        self.role = role

    def update_branch_id(self, branch_id: int) -> None:
        self.branch_id = branch_id