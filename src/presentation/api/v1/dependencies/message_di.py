from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.domain.interfaces.message_repo import MessageRepository
from src.core.domain.interfaces.order_repo import OrderRepository
from src.infrastructure.database.repositories.message_repo_impl import MessageRepositoryImpl
from src.infrastructure.database.dao.message_dao import MessageDAO
from src.presentation.api.v1.dependencies.dependencies import get_db_session
from src.presentation.api.v1.dependencies.order_di import get_order_repo

from src.core.application.use_cases.get_messages_use_case import GetMessagesUseCase
from src.core.application.use_cases.post_message_use_case import PostMessageUseCase

def get_message_repo(session: AsyncSession = Depends(get_db_session)) -> MessageRepository:
    return MessageRepositoryImpl(message_dao = MessageDAO(session))

def get_messages_use_case_di(
        message_repo: MessageRepository = Depends(get_message_repo),
        order_repo: OrderRepository = Depends(get_order_repo),
        ):
    return GetMessagesUseCase(message_repo=message_repo, order_repo=order_repo)

def post_message_use_case_di(
        message_repo: MessageRepository = Depends(get_message_repo),
        order_repo: OrderRepository = Depends(get_order_repo),
        ):
    return PostMessageUseCase(message_repo=message_repo, order_repo=order_repo)