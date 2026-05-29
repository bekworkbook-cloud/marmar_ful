import json
import hmac
import hashlib

from typing import AsyncGenerator, Callable
from urllib.parse import parse_qsl

from fastapi import Header, HTTPException, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.infrastructure.database.dao.user_dao import UserDAO
from src.infrastructure.database.models.base import async_session_maker
from src.infrastructure.database.repositories.user_repo_impl import UserRepositoryImpl
from src.core.domain.entities.user import User
from src.core.domain.enums.roles import UserRole
from src.core.domain.enums.permissions import Permission


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


def verify_webapp_signature(role: UserRole) -> Callable:
    async def decorator(x_telegram_init_data: str = Header(...)) -> dict:
        try:
            parsed_data = dict(parse_qsl(x_telegram_init_data, strict_parsing=True))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid init data format")
        
        received_hash = parsed_data.pop("hash", None)
        if not received_hash:
            raise HTTPException(status_code=400, detail="Hash is missing")
            
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed_data.items()))
        bot_token = settings.get_bot_token(role)
        secret_key = hmac.new("WebAppData".encode(), bot_token.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        
        if not hmac.compare_digest(calculated_hash, received_hash):
            raise HTTPException(status_code=401, detail="Invalid signature")
            
        return parsed_data
        
    return decorator

async def get_authenticated_user(
    role: UserRole,
    init_data: dict,
    session: AsyncSession
) -> User:
    user_data_str = init_data.get("user")
    if not user_data_str:
        raise HTTPException(status_code=401, detail="User data missing")
        
    try:
        user_data = json.loads(user_data_str)
        telegram_id = int(user_data.get("id"))
    except (json.JSONDecodeError, ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid user data format")

    repo = UserRepositoryImpl(UserDAO(session))
    user = await repo.get_by_telegram_id(telegram_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user

def require_permission(role: UserRole, permission: Permission) -> Callable:
    async def permission_checker(
        init_data: dict = Depends(verify_webapp_signature(role)),
        session: AsyncSession = Depends(get_db_session)
    ) -> User:
        user = await get_authenticated_user(role, init_data, session)
        if not user.has_permission(permission):
            raise HTTPException(status_code=403, detail="Forbidden: insufficient permissions")
        return user
    return permission_checker
