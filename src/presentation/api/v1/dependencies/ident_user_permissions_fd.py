from fastapi import HTTPException, status, Depends
from src.core.domain.enums.permissions import Permission
from src.core.domain.enums.roles import UserRole
from src.presentation.api.v1.dependencies.auth import get_token_data
from src.core.domain.services.access_control import ROLE_PERMISSIONS
from src.shared.dto.auth_dto import TokenDataDTO

class PermissionChecker:
    def __init__(self, required_permission: Permission):
        self.required_permission = required_permission

    async def __call__(self, token_data: TokenDataDTO = Depends(get_token_data)):
        user_role_str = token_data.user_role
        print("here")
        
        try:
            user_role = UserRole(user_role_str)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail=f"Unknown user role: {user_role_str}"
            )

        # 2. Получаем список разрешений для этой роли
        allowed_permissions = ROLE_PERMISSIONS.get(user_role, set())
        # 3. Проверяем, есть ли нужный пермишен
        if self.required_permission not in allowed_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="У вас недостаточно прав для выполнения этого действия"
            )
        
        return token_data
