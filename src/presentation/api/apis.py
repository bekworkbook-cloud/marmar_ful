from fastapi import APIRouter

from .v1.main_router import api_router as api_router_v1



api_router = APIRouter(prefix="/api")


api_router.include_router(api_router_v1)