from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.domain.interfaces.order_repo import OrderRepository
from src.core.domain.interfaces.order_item_repo import OrderItemRepository
from src.core.domain.interfaces.product_repo import ProductRepository
from src.core.domain.interfaces.user_repo import UserRepository
from src.infrastructure.database.repositories.order_repo_impl import OrderRepositoryImpl
from src.infrastructure.database.dao.order_dao import OrderDAO
from src.presentation.api.v1.dependencies.dependencies import get_db_session
from src.presentation.api.v1.dependencies.order_item_di import get_order_item_repo
from src.presentation.api.v1.dependencies.product_di import get_product_repo
from src.presentation.api.v1.dependencies.user_di import get_user_repo

from src.core.application.use_cases.get_orders_use_case import GetOrdersUseCase
from src.core.application.use_cases.get_order_use_case import GetOrderUseCase
from src.core.application.use_cases.post_order_use_case import PostOrderUseCase
from src.core.application.use_cases.put_order_use_case import PutOrderUseCase
from src.core.application.use_cases.patch_order_courier_use_case import PatchOrderCourierUseCase
from src.core.application.use_cases.patch_order_payment_use_case import PatchOrderPaymentUseCase
from src.core.application.use_cases.patch_order_status_use_case import PatchOrderStatusUseCase
from src.core.application.use_cases.patch_order_accept_use_case import PatchOrderAcceptUseCase
from src.core.application.use_cases.patch_order_operator_use_case import PatchOrderOperatorUseCase


def get_order_repo(session: AsyncSession = Depends(get_db_session)) -> OrderRepository:
    return OrderRepositoryImpl(order_dao = OrderDAO(session))





def get_orders_use_case_di(
        order_repo: OrderRepository = Depends(get_order_repo),
        user_repo: UserRepository = Depends(get_user_repo)
        ):
    return GetOrdersUseCase(order_repo, user_repo)

def get_order_use_case_di(
        order_repo: OrderRepository = Depends(get_order_repo),
        user_repo: UserRepository = Depends(get_user_repo)
        ):
    return GetOrderUseCase(
        order_repo=order_repo,
        user_repo=user_repo
    )

def post_order_use_case_di(
        order_repo: OrderRepository = Depends(get_order_repo),
        order_item_repo: OrderItemRepository = Depends(get_order_item_repo),
        product_repo: ProductRepository = Depends(get_product_repo),
        user_repo: UserRepository = Depends(get_user_repo)
        ):
    return PostOrderUseCase(
        order_repo=order_repo,
        order_item_repo=order_item_repo,
        product_repo=product_repo,
        user_repo=user_repo
    )

def put_order_use_case_di(repo: OrderRepository = Depends(get_order_repo)):
    return PutOrderUseCase(repo)

def patch_order_courier_use_case_di(repo: OrderRepository = Depends(get_order_repo)):
    return PatchOrderCourierUseCase(repo)

def patch_order_payment_use_case_di(repo: OrderRepository = Depends(get_order_repo)):
    return PatchOrderPaymentUseCase(repo)

def patch_order_status_use_case_di(repo: OrderRepository = Depends(get_order_repo)):
    return PatchOrderStatusUseCase(repo)

def patch_order_accept_use_case_di(repo: OrderRepository = Depends(get_order_repo)):
    return PatchOrderAcceptUseCase(repo)

def patch_order_operator_use_case_di(repo: OrderRepository = Depends(get_order_repo)):
    return PatchOrderOperatorUseCase(repo)
