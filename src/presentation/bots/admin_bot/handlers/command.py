from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from src.core.application.use_cases.verify_admin_access import VerifyAdminAccessUseCase
from src.core.domain.exceptions.access import DomainAccessDeniedError
from src.core.application.use_cases.dtos.auth_dtos import UserTelegramDTO
from ..keyboards.inline import InliineKB as ikb

router = Router()


@router.message(CommandStart())
async def cmd_start(msg: Message, use_case: VerifyAdminAccessUseCase):
    user = msg.from_user
    user_dto = UserTelegramDTO(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name
    )
    try:
        await use_case.execute(user_telegram_dto=user_dto)
    
        text = (
            "Привет, админ\n"
            "Перейдите на панель администратора по кнопке ниже\n"
        )
        await msg.answer(text, reply_markup=ikb.get_mini_app_button())
    except DomainAccessDeniedError:
        await msg.answer("У вас недостаточно прав для выполнения этой команды.")
