from aiogram import Router

from .command import router as command_router


customer_router = Router()
customer_router.include_router(command_router)
