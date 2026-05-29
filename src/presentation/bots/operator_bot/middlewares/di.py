from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable
from src.infrastructure.database.dao.user_dao import UserDAO
from src.infrastructure.database.repositories.user_repo_impl import UserRepositoryImpl
from src.core.application.use_cases.verify_operator_access_use_case import VerifyOperatorAccessUseCase

class DIMiddleware(BaseMiddleware):
    def __init__(self, session_maker):
        self.session_maker = session_maker

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with self.session_maker() as session:
            user_dao = UserDAO(session)
            user_repo = UserRepositoryImpl(user_dao)
            data["use_case"] = VerifyOperatorAccessUseCase(user_repo)
            return await handler(event, data)