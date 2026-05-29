from fastapi import APIRouter

from .routers.branches_and_menu import router as branch_router
from .routers.categories import router as category_router
from .routers.chat_message import router as chat_message_router
from .routers.products import router as porduct_router
from .routers.orders_and_order_items import router as order_router
from .routers.users import router as user_router
from .routers.auth import router as auth_router


api_router = APIRouter(prefix='/v1')
api_router.include_router(branch_router)
api_router.include_router(category_router)
api_router.include_router(chat_message_router)
api_router.include_router(order_router)
api_router.include_router(porduct_router)
api_router.include_router(user_router)
api_router.include_router(auth_router)

