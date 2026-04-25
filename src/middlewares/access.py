import typing
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.dispatcher.flags import get_flag
from src.core.domain.exceptions.access import DomainAccessDeniedError

class AccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: typing.Callable[[TelegramObject, typing.Dict[str, typing.Any]], typing.Awaitable[typing.Any]],
        event: TelegramObject,
        data: typing.Dict[str, typing.Any]
    ) -> typing.Any:
        required_permission = get_flag(data, "permission")
        
        if required_permission:
            user = data.get("current_user")
            
            if not user:
                return
                
            try:
                user.require_permission(required_permission)
            except DomainAccessDeniedError:
                return
                
        return await handler(event, data)
