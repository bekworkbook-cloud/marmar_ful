from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from src.core.application.use_cases.verify_courier_access import VerifyCourierAccessUseCase
from src.core.domain.exceptions.access import DomainAccessDeniedError
from ..keyboards.inline import InlineKb as ikb


router = Router()


@router.message(CommandStart())
async def cmd_start(msg: Message, use_case: VerifyCourierAccessUseCase):
    try:
        await use_case.execute(telegram_id=msg.from_user.id)
        text = (
            f"Привет, {msg.from_user.first_name}\n"
            f"перейдите на вебприложение по кнопку ниже\n"
        )
        await msg.answer(text, reply_markup=ikb.get_mini_app_kb())

    except DomainAccessDeniedError:
        await msg.answer("У вас не достаточно доступа для этой сообшение")
