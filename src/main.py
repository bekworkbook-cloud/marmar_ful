import logging
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from aiogram.exceptions import TelegramRetryAfter
from aiogram import Bot

from src.config import settings, bots
from src.webhook import webhook_router
from src.middlewares.access import AccessMiddleware

from src.infrastructure.database.models.base import async_session_maker

from src.presentation.api.admin import router as admin_api_router
from src.presentation.bots.admin_bot.handlers import admin_router
from src.presentation.bots.admin_bot.middlewares.di import DIMiddleware as admin_dim
from src.presentation.bots.customer_bot.handlers import customer_router
from src.presentation.bots.customer_bot.middlewares.di import DIMiddleware as customer_dim
from src.presentation.bots.courier_bot.handlers import courier_router
from src.presentation.bots.courier_bot.middlewares.di import DIMiddleware as courier_dim
from src.presentation.bots.operator_bot.handlers import operator_router
from src.presentation.bots.operator_bot.middlewares.di import DIMiddleware as operator_dim


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


bots.dispatchers["admin_bot"].message.middleware(admin_dim())
bots.dispatchers["admin_bot"].message.middleware(AccessMiddleware())
bots.dispatchers["admin_bot"].include_router(admin_router)


bots.dispatchers["courier_bot"].message.middleware(courier_dim(async_session_maker))
bots.dispatchers["courier_bot"].message.middleware(AccessMiddleware())
bots.dispatchers["courier_bot"].include_router(courier_router)

bots.dispatchers["customer_bot"].message.middleware(customer_dim(async_session_maker))
bots.dispatchers["customer_bot"].message.middleware(AccessMiddleware())
bots.dispatchers["customer_bot"].include_router(customer_router)

bots.dispatchers["operator_bot"].message.middleware(operator_dim(async_session_maker))
bots.dispatchers["operator_bot"].message.middleware(AccessMiddleware())
bots.dispatchers["operator_bot"].include_router(operator_router)

async def ensure_webhook(bot_id: str, bot: Bot, dispatcher):
    webhook_url = f"{settings.get_webhook_url()}/{bot_id}"
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_webhook(url=webhook_url, drop_pending_updates=True)
        logging.info(f"[{bot_id}] Webhook set")
    except Exception as e:
        logging.error(f"[{bot_id}] Webhook setup failed: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    for bot_id, bot in bots.bots.items():
        dispatcher = bots.dispatchers[bot_id]
        await ensure_webhook(bot_id, bot, dispatcher)
    yield
    for bot_id, bot in bots.bots.items():
        await bot.delete_webhook()
        await bot.session.close()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="src/static"), name="static")
app.include_router(webhook_router)
app.include_router(admin_api_router)

