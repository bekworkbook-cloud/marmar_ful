import logging

from fastapi import APIRouter, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, Response
from fastapi.requests import Request

from src.infrastructure.database.dao.user_dao import UserDAO

from src.core.domain.enums.roles import UserRole


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
logger = logging.getLogger(__name__)


@router.get("/")
async def get_loader(request: Request):
    return templates.TemplateResponse("loader.html", {"request": request})

@router.post("/auth")
async def auth_user(request: Request, response: Response):
    body = await request.json()
    user = body.get("user")
    
    if not user or 'id' not in user:
        raise HTTPException(status_code=400, detail="User data missing")

    role = await UserDAO.get_role_by_telegram_id(user['id'])
    
    if role:
        response.set_cookie(key="tg_user_id", value=str(user['id']), httponly=True)
        return {"status": "ok", "role": role}
    else:
        raise HTTPException(status_code=401, detail="User not found")

async def get_current_user(request: Request):
    """Утилита для получения пользователя из кук, чтобы не дублировать код."""
    tg_id = request.cookies.get("tg_user_id")
    if not tg_id:
        return None
    return await UserDAO.find_one_or_none(telegram_id=int(tg_id))

@router.get("/main")
async def main_page(request: Request):
    user = await get_current_user(request)
    if not user:
        return RedirectResponse(url="/webapp/forbidden", status_code=303)
    

    if user.role == UserRole.ADMIN.value:
        return RedirectResponse(url="/webapp/admin", status_code=303)
    
    elif user.role == UserRole.MAINOPERATOR.value:
        return RedirectResponse(url="/webapp/main_operator", status_code=303)
    
    elif user.role == UserRole.OPERATOR.value:
        return RedirectResponse(url="/webapp/operator", status_code=303)
    
    elif user.role == UserRole.COURIER.value:
        return RedirectResponse(url="/webapp/courier", status_code=303)

    elif user.role == UserRole.CUSTOMER.value:
        return RedirectResponse(url="/webapp/customer")
    
    else:
        logger.warning("Unknown role for user %s: %r", user.id, user.role)
        return RedirectResponse(url="/webapp/forbidden", status_code=303)


@router.get("/forbidden")
async def forbidden_page(request: Request):
    return templates.TemplateResponse("forbidden.html", {"request": request})
