from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from src.core.application.use_cases.verify_customer_access import VerifyCustomerAccessUseCase
from src.core.domain.exceptions.access import DomainAccessDeniedError
from ..keyboards.inline import InlineKb as ikb

from src.core.application.use_cases.dtos.auth_dtos import UserTelegramDTO


router = Router()


@router.message(CommandStart())
async def cmd_start(msg: Message, use_case: VerifyCustomerAccessUseCase):
    try:
        user = msg.from_user
        user_telegram_dto = UserTelegramDTO(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name
        )
        await use_case.execute(user_telegram_dto=user_telegram_dto)
        text = (
            f"Привет, {msg.from_user.first_name}\n"
            f"перейдите на вебприложение по кнопку ниже\n"
        )
        await msg.answer(text, reply_markup=ikb.get_mini_app_kb())

    except DomainAccessDeniedError:
        await msg.answer("У вас не достаточно доступа для этой сообшение")
