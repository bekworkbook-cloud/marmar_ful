from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from src.core.domain.exceptions.access import DomainAccessDeniedError
from src.core.application.use_cases.verify_operator_access_use_case import VerifyOperatorAccessUseCase
from src.shared.dto.auth_dto import UserTelegramDTO
from ..keyboards.inline import InliineKB as ikb


router = Router()


@router.message(CommandStart())
async def cmd_start(msg: Message, use_case: VerifyOperatorAccessUseCase):
    telegram_user = msg.from_user
    user_telegram_dto = UserTelegramDTO(
        telegram_id=telegram_user.id,
        username=telegram_user.username,
        first_name=telegram_user.first_name        
    )

    try:
        await use_case.execute(user_telegram_dto)  
        text = "text" # welcome text for operators
        await msg.answer(text=text, reply_markup=ikb.get_mini_app_button()) 
    except DomainAccessDeniedError:
        await msg.answer("У вас не достаточно прав")

