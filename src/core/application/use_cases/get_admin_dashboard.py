
from src.core.domain.enums.permissions import Permission
from src.shared.dto.admin_dashboard import AdminDashboardResponseDTO

class GetAdminDashboardUseCase:
    def __init__(self, user_repo, order_repo):
        self.user_repo = user_repo
        self.order_repo = order_repo

    async def execute(self, dto):
        # Вызываем get_by_id, так как метода get не существует
        user = await self.user_repo.get_by_id(dto.user_id)
        
        if not user:
            raise ValueError("Admin not found")

        user.require_permission(Permission.VIEW_ADMIN_DASHBOARD)

        # Все вызовы репозитория должны быть с await
        users_count = await self.user_repo.count_all()
        active_orders = await self.order_repo.count_active()
        revenue_today = await self.order_repo.revenue_today()

        return AdminDashboardResponseDTO(
            users_count=users_count,
            active_orders=active_orders,
            revenue_today=revenue_today
        )