from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from src.core.application.use_cases.get_admin_dashboard import GetAdminDashboardUseCase
from src.shared.dto.admin_dashboard import AdminDashboardDTO
from src.core.domain.enums.permissions import Permission
from src.core.domain.entities.user import User
from src.core.domain.enums.roles import UserRole
from src.presentation.api.dependencies import require_permission, get_admin_dashboard_use_case

router = APIRouter(prefix="/webapp/admin_bot")
templates = Jinja2Templates(directory="src/presentation/bots/admin_bot/mini_app_templates")


@router.get("/")
async def admin_loader(request: Request):

    return templates.TemplateResponse(request, "loader.html")


@router.get("/dashboard")
async def admin_dashboard(
    request: Request,
    # Фабрика сама проверит подпись токеном админ-бота и вернет пользователя
    current_user: User = Depends(require_permission(UserRole.ADMIN, Permission.VIEW_ADMIN_DASHBOARD)),
    use_case = Depends(get_admin_dashboard_use_case)
):
    dto = AdminDashboardDTO(user_id=current_user.id)
    result = await use_case.execute(dto)
    
    return templates.TemplateResponse(
        request, 
        "dashboard.html", 
        {"data": result, "user": current_user}
    )