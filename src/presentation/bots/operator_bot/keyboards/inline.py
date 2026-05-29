from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from src.config import settings



class InliineKB:

    @staticmethod
    def get_mini_app_button():
        builder = InlineKeyboardBuilder()
        builder.button(text="Открывать админ панель", web_app=WebAppInfo(url=f"{settings.get_webapp_url()}/in/operator_bot/"))
        
        return builder.as_markup()
    