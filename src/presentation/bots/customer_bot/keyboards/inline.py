from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from src.config import settings

class InlineKb:

    @staticmethod
    def get_mini_app_kb():
        builder = InlineKeyboardBuilder()
        builder.button(text="Открыть веб страницу", web_app=WebAppInfo(url=f"{settings.get_webapp_url()}/customer_bot"))
        return builder.as_markup()