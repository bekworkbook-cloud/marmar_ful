import enum

import bcrypt
from pydantic_settings import BaseSettings, SettingsConfigDict
from aiogram import Bot, Dispatcher
from src.core.domain.enums.roles import UserRole
from fastapi.security import OAuth2PasswordBearer

class Settings(BaseSettings):
    ADMIN_BOT_TOKEN: str
    COURIER_BOT_TOKEN: str
    CUSTOMER_BOT_TOKEN: str
    OPERATOR_BOT_TOKEN: str
    BASE_SITE_URL: str
    ADMIN_TELEGRAM_ID: int
    API_URL: str
    API_PASS: str
    API_BRANCHES: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str

    CLICK_TEST_TOKEN: str
    PAYCOM_TEST_TOKEN: str

    PAYCOM_LIVE_TOKEN: str
    CLICK_LIVE_TOKEN: str
    

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def get_webhook_url(self) -> str:
        return f"{self.BASE_SITE_URL}/webhook"

    def get_webapp_url(self) -> str:
        return f"{self.BASE_SITE_URL}/webapp"

    def get_bot_token(self, role: enum) -> str:
        if role == UserRole.ADMIN:
            return self.ADMIN_BOT_TOKEN
        elif role == UserRole.OPERATOR or role==UserRole.MAINOPERATOR:
            return self.OPERATOR_BOT_TOKEN
        elif role == UserRole.COURIER:
            return self.COURIER_BOT_TOKEN
        else:
            return self.CUSTOMER_BOT_TOKEN

class Bots:
    def __init__(self, settings: Settings):
        self.bots = {
            "admin_bot": Bot(settings.ADMIN_BOT_TOKEN),
            "courier_bot": Bot(settings.COURIER_BOT_TOKEN),
            "customer_bot": Bot(settings.CUSTOMER_BOT_TOKEN),
            "operator_bot": Bot(settings.OPERATOR_BOT_TOKEN),
        }
        self.dispatchers = {
            "admin_bot": Dispatcher(),
            "courier_bot": Dispatcher(),
            "customer_bot": Dispatcher(),
            "operator_bot": Dispatcher(),
        }
        self.bot_tokens = {
            "admin_bot": settings.ADMIN_BOT_TOKEN,
            "courier_bot": settings.COURIER_BOT_TOKEN,
            "customer_bot": settings.CUSTOMER_BOT_TOKEN,
            "operator_bot": settings.OPERATOR_BOT_TOKEN,
        }

class AuthPwd:
    def __init__(self):
        self.oauth2_schema = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/token')


settings = Settings()
bots = Bots(settings)

auth_pwd = AuthPwd()
