from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from src.core.application.use_cases.verify_admin_access import VerifyAdminAccessUseCase
from src.core.domain.exceptions.access import DomainAccessDeniedError
from ..keyboards.inline import InliineKB as ikb

router = Router()

@router.message(CommandStart())
async def cmd_start(msg: Message, use_case: VerifyAdminAccessUseCase):
    try:
        await use_case.execute(telegram_id=msg.from_user.id)
        
        text = (
            "Привет, админ\n"
            "Перейдите на панель администратора по кнопке ниже\n"
        )
        await msg.answer(text, reply_markup=ikb.get_mini_app_button())
    except DomainAccessDeniedError:
        await msg.answer("У вас недостаточно прав для выполнения этой команды.")