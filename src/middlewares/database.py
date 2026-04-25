import typing
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from src.infrastructure.database.models.base import async_session_maker

class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: typing.Callable[[TelegramObject, typing.Dict[str, typing.Any]], typing.Awaitable[typing.Any]],
        event: TelegramObject,
        data: typing.Dict[str, typing.Any]
    ) -> typing.Any:
        async with async_session_maker() as session:
            data["session"] = session
            return await handler(event, data)
