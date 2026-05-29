from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.domain.interfaces.payment_log_repo import PaymentLogRepository
from src.infrastructure.database.repositories.payment_log_repo_impl import PaymentLogRepositoryImpl
from src.infrastructure.database.dao.payment_log_dao import PaymentLogDAO
from src.presentation.api.v1.dependencies.dependencies import get_db_session

from src.core.application.use_cases.get_payment_logs_use_case import GetPaymentLogsUseCase
from src.core.application.use_cases.get_payment_log_use_case import GetPaymentLogUseCase
from src.core.application.use_cases.patch_payment_log_use_case import PatchPaymentLogUseCase


def get_payment_log_repo(session: AsyncSession = Depends(get_db_session)) -> PaymentLogRepository:
    return PaymentLogRepositoryImpl(payment_log_dao = PaymentLogDAO(session))

def get_payment_logs_use_case_di(repo: PaymentLogRepository = Depends(get_payment_log_repo)):
    return GetPaymentLogsUseCase(repo)

def get_payment_log_use_case_di(repo: PaymentLogRepository = Depends(get_payment_log_repo)):
    return GetPaymentLogUseCase(repo)

def patch_payment_log_use_case_di(repo: PaymentLogRepository = Depends(get_payment_log_repo)):
    return PatchPaymentLogUseCase(repo)