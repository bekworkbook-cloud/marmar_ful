import typing
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from src.infrastructure.database.models.base import async_session_maker
from src.infrastructure.database.dao.user_dao import UserDAO
from src.infrastructure.database.repositories.user_repo_impl import UserRepositoryImpl
from src.core.application.use_cases.verify_admin_access import VerifyAdminAccessUseCase


class DIMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: typing.Callable[[TelegramObject, typing.Dict[str, typing.Any]], typing.Awaitable[typing.Any]],
        event: TelegramObject,
        data: typing.Dict[str, typing.Any]
    ) -> typing.Any:
    
        async with async_session_maker() as session:
            user_dao = UserDAO(session)
            user_repo = UserRepositoryImpl(user_dao)
            data["user_repo"] = user_repo
            data["use_case"] = VerifyAdminAccessUseCase(user_repo)
            
            return await handler(event, data)
