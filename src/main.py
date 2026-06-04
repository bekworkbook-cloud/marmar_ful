import logging
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot


from src.config import settings, bots
from src.webhook import webhook_router
from src.middlewares.access import AccessMiddleware

from src.infrastructure.database.models.base import async_session_maker

from src.presentation.api.apis import api_router
from src.presentation.api.exceptions.exceptions import register_exception_handlers

from src.presentation.bots.admin_bot.handlers import admin_router
from src.presentation.bots.admin_bot.middlewares.di import DIMiddleware as admin_dim
from src.presentation.bots.customer_bot.handlers import customer_router
from src.presentation.bots.customer_bot.middlewares.di import DIMiddleware as customer_dim
from src.presentation.bots.courier_bot.handlers import courier_router
from src.presentation.bots.courier_bot.middlewares.di import DIMiddleware as courier_dim
from src.presentation.bots.operator_bot.handlers import operator_router
from src.presentation.bots.operator_bot.middlewares.di import DIMiddleware as operator_dim

from src.presentation.bots.pages.input_points import router as input_pages_router


from src.core.application.exceptions.not_found_exception import NotFoundException
from fastapi.responses import JSONResponse
from fastapi import Request





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


app = FastAPI(lifespan=lifespan, swagger_ui_parameters={"persistAuthorization": True})
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает запросы абсолютно со всех источников (включая iOS WebKit)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешает все методы: GET, POST, PUT, PATCH, DELETE, OPTIONS
    allow_headers=["*"],  # Разрешает все заголовки, включая твой Authorization и Content-Type
)
@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.mount("/webapp/in/customer_bot", StaticFiles(directory="static/customer", html=True), name="customer_bot")
app.mount("/webapp/in/operator_bot", StaticFiles(directory="static/operator", html=True), name="operator_bot")
app.mount("/webapp/in/courier_bot", StaticFiles(directory="static/courier", html=True), name="courier_bot")
app.mount("/webapp/in/admin_bot", StaticFiles(directory="static/admin", html=True), name="admin_bot")
app.include_router(webhook_router)
app.include_router(api_router)
app.include_router(input_pages_router)
register_exception_handlers(app)

