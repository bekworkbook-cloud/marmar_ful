from aiogram import Router
from .command import router as command_router

courier_router = Router()
courier_router.include_router(command_router)