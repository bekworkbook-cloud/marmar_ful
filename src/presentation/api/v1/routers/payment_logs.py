from fastapi import APIRouter, Depends
from src.presentation.api.v1.dependencies.ident_user_permissions_fd import PermissionChecker
from src.presentation.api.v1.dependencies.auth import check_token
from src.core.domain.enums.permissions import Permission
from src.core.application.use_cases.get_payment_logs_use_case import GetPaymentLogsUseCase
from src.core.application.use_cases.get_payment_log_use_case import GetPaymentLogUseCase
from src.core.application.use_cases.patch_payment_log_use_case import PatchPaymentLogUseCase

from src.core.application.use_cases.dtos.payment_log_dtos import (
    PaymentLogDTO,
    PaymentLogsDTO,
    PaymentLogCreateDTO
)

from src.presentation.api.v1.dependencies.payment_log_di import (
    get_payment_logs_use_case_di,
    get_payment_log_use_case_di,
    patch_payment_log_use_case_di,
)




router = APIRouter(prefix="/payments", tags=["Payments"])

'''
payment logs (Логи платежей)
{ GET: /payment_logs , role{admin, main_operator}, query_parameters{order_id, branch_id, courier_id, limit, offset} }
{ GET: /payment_logs/{payment_log_id} , role{admin, main_operator}, query_parameters{} }
{ PATCH: /payment_logs/{payment_log_id} , role{admin, main_operator}, query_parameters{} }
'''

@router.get(
        "/", 
        dependencies=[Depends(PermissionChecker(Permission.GET_PAYMENT_LOGS))],
        response_model=PaymentLogsDTO
    )
async def get_payment_logs(
    order_id: int = None,
    branch_id: int = None,
    courier_id: int = None,
    limit: int = 10,
    offset: int = 0,
    token: str = Depends(check_token),
    use_case: GetPaymentLogsUseCase = Depends(get_payment_logs_use_case_di)
):
    return await use_case.execute(order_id, branch_id, courier_id, limit, offset)   

@router.get(
        "/{payment_log_id}", 
        dependencies=[Depends(PermissionChecker(Permission.GET_PAYMENT_LOGS))],
        response_model=PaymentLogDTO
    )
async def get_payment_log(
    payment_log_id: int,
    token: str = Depends(check_token),
    use_case: GetPaymentLogUseCase = Depends(get_payment_log_use_case_di)
):
    return await use_case.execute(payment_log_id)

@router.patch(
        "/{payment_log_id}", 
        dependencies=[Depends(PermissionChecker(Permission.UPDATE_PAYMENT_LOGS))],
        response_model=PaymentLogDTO
    )
async def patch_payment_log(
    payment_log_id: int,
    payment_log: PaymentLogCreateDTO,
    token: str = Depends(check_token),
    use_case: PatchPaymentLogUseCase = Depends(patch_payment_log_use_case_di)
):
    return await use_case.execute(payment_log_id, payment_log)