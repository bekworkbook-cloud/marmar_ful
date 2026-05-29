import hmac
import json
import hashlib

from urllib.parse import parse_qsl
from fastapi import Header, Depends
from fastapi.exceptions import HTTPException
from src.config import settings, bots
from src.presentation.api.v1.dependencies.user import get_user_repo
from src.core.application.use_cases.verify_web_app_signature import VerifyWebAppSignatureUseCase
from src.core.domain.interfaces.user_repo import UserRepository

from src.core.domain.services.auth_service import AuthService
from src.presentation.api.v1.dependencies.services import get_auth_service


def verify_webapp_signature_dynamic(
    bot: str,
    x_telegram_init_data: str = Header(...)
) -> dict:
    tg_bot = bots.bots.get(bot)
    if not tg_bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    try:
        parsed_data = dict(parse_qsl(x_telegram_init_data, strict_parsing=True))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid init data format")
    
    received_hash = parsed_data.pop("hash", None)
    if not received_hash:
        raise HTTPException(status_code=400, detail="Hash is missing")
        
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed_data.items()))
    
    secret_key = hmac.new(b"WebAppData", tg_bot.token.encode(), hashlib.sha256).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    
    if not hmac.compare_digest(calculated_hash, received_hash):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    for key in ["user", "receiver", "chat"]:
        if key in parsed_data:
            try:
                parsed_data[key] = json.loads(parsed_data[key])
            except (ValueError, TypeError):
                pass
                
    return parsed_data

def verify_webapp_signature_use_case(
        repo: UserRepository = Depends(get_user_repo),
        auth: AuthService = Depends(get_auth_service)
        ) -> VerifyWebAppSignatureUseCase:
    return VerifyWebAppSignatureUseCase(user_repo=repo, auth_service=auth)
