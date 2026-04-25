from aiogram import Router
from .command import router as command_router

admin_router = Router()
admin_router.include_router(command_router)