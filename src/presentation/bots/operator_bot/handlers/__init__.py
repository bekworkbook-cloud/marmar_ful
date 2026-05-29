from aiogram import Router
from .command import router as command_router

operator_router = Router()
operator_router.include_router(command_router)
