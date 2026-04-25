
from src.core.domain.enums.roles import UserRole
from src.core.domain.enums.permissions import Permission


ROLE_PERMISSIONS = {
    UserRole.CUSTOMER: {
        Permission.CREATE_ORDER,
        Permission.ACCESS_CUSTOMER_CHAT,
    },
    UserRole.COURIER: {
        Permission.VIEW_ALL_ORDERS,
        Permission.ACCESS_COURIER_CHAT,
    },
    UserRole.OPERATOR: {
        Permission.CREATE_ORDER,
        Permission.UPDATE_ORDER,
        Permission.VIEW_CUSTOMER_PAGE,
        Permission.ACCESS_OPERATOR_CHAT,
    },
    UserRole.MAINOPERATOR: {
        Permission.CREATE_ORDER,
        Permission.UPDATE_ORDER,
        Permission.DELETE_ORDER,
        Permission.ACCESS_OPERATOR_CHAT,
    },
    UserRole.ADMIN: {
        Permission.CREATE_ORDER,
        Permission.UPDATE_ORDER,
        Permission.DELETE_ORDER,
        Permission.ASSIGN_COURIER,
        Permission.VIEW_ALL_ORDERS,
        Permission.VIEW_ADMIN_DASHBOARD,
        Permission.ACCESS_ADMIN_CHAT,
    },
}



class AccessControlService:

    def has_permission(self, role: UserRole, permission: Permission) -> bool:
        return permission in ROLE_PERMISSIONS.get(role, set())
    
    