from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from src.core.application.use_cases.verify_courier_access_use_case import VerifyCourierAccessUseCase
from src.core.domain.exceptions.access import DomainAccessDeniedError
from ..keyboards.inline import InlineKb as ikb
from src.shared.dto.auth_dto import UserTelegramDTO


router = Router()


@router.message(CommandStart())
async def cmd_start(msg: Message, use_case: VerifyCourierAccessUseCase):
    telegram_user = msg.from_user
    telegram_user_dto = UserTelegramDTO(
        telegram_id=telegram_user.id,
        username=telegram_user.username,
        first_name=telegram_user.first_name
    )
    try:
        await use_case.execute(telegram_user_dto)
        text = (
            f"Привет, {msg.from_user.first_name}\n"
            f"перейдите на вебприложение по кнопку ниже\n"
        )
        await msg.answer(text, reply_markup=ikb.get_mini_app_kb())

    except DomainAccessDeniedError:
        await msg.answer("У вас не достаточно доступа для этой сообшение")
