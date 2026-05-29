import json
from pathlib import Path
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.exceptions import HTTPException

from src.presentation.api.v1.dependencies.init_data import verify_webapp_signature_dynamic
from src.core.application.use_cases.verify_web_app_signature import VerifyWebAppSignatureUseCase
from src.presentation.api.v1.dependencies.init_data import verify_webapp_signature_use_case
from src.core.application.use_cases.dtos.auth_dtos import UserTelegramDTO


file_pathes = {
    "admin_bot": "src/static/pages/admin/",
    "operator_bot": "src/static/pages/operator/",
    "courier_bot": "src/static/pages/courier/",
    "customer_bot": "src/static/pages/customer/"
}

BOT_REACT_PATHS = { 
    "admin_bot": "static/admin/", 
    "operator_bot": "static/operator/", 
    "courier_bot": "static/courier/", 
    "customer_bot": "static/customer/" 
}




router = APIRouter(prefix="/webapp", tags=["tg bot inputpages"], include_in_schema=False)



@router.get("/in/{bot}")
async def get_input_pages(bot: str):
    # 2. Изменено имя переменной во избежание конфликта областей видимости
    bot_path = BOT_REACT_PATHS.get(bot)
    
    # 3. Исправлена опечатка в проверке (было file_pathes)
    if bot_path is None:
        raise HTTPException(status_code=404, detail="File not found")
        
    # 4. Исправлен путь: bot_path — это уже строка, метод .get() тут не нужен
    file_path = Path(bot_path) / "index.html"
    
    # Дополнительная проверка: существует ли файл физически на сервере
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Static file index.html not found on server")
        
    return FileResponse(path=file_path)


@router.post("/auth/{bot}")
async def tg_init_data(
    init_data: dict = Depends(verify_webapp_signature_dynamic),
    use_case: VerifyWebAppSignatureUseCase = Depends(verify_webapp_signature_use_case)
    ):
    user = init_data.get("user")
    user_telegram_dto = UserTelegramDTO(
        telegram_id=user['id'],
        username=user['username'],
        first_name=user['first_name']
    )

    return await use_case.execute(user_telegram_dto)


@router.get("/app/{bot}")
async def get_app_admin_page(bot: str):
    file_path = file_pathes.get(bot)
    if file_path is None:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )
    
    return FileResponse(path=Path(file_path, "index.html"))



