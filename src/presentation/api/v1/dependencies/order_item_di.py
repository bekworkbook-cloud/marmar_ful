from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.domain.interfaces.order_item_repo import OrderItemRepository
from src.infrastructure.database.repositories.order_item_repo_impl import OrderItemRepositoryImpl
from src.infrastructure.database.dao.order_item_dao import OrderItemDAO
from src.presentation.api.v1.dependencies.dependencies import get_db_session

from src.core.application.use_cases.get_order_items_use_case import GetOrderItemsUseCase


def get_order_item_repo(session: AsyncSession = Depends(get_db_session)) -> OrderItemRepository:
    return OrderItemRepositoryImpl(order_item_dao = OrderItemDAO(session))  

def get_order_items_use_case_di(repo: OrderItemRepository = Depends(get_order_item_repo)):
    return GetOrderItemsUseCase(repo)