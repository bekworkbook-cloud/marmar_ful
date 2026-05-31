from fastapi import APIRouter, Depends, HTTPException
from src.presentation.api.v1.dependencies.ident_user_permissions_fd import PermissionChecker
from src.presentation.api.v1.dependencies.auth import check_token, get_token_data
from src.core.domain.enums.permissions import Permission
from src.core.application.use_cases.dtos.order_dtos import (
    OrderCreateDTO,
    GetOrdersInputDTO,
    GetOrderInputDTO,
    OrderUpdateRequest,
    UpdateOrderInputDTO,
    OrderPersonnelUpdateDTO,
    OrderPersonnelIdsDTO,
    OrderPaymentUpdateDTO,
    OrderPaymentMethodDTO,
    OrderStatusUpdateDTO,
    OrderStatusDTO,
    OrderAcceptUpdateDTO,
    OrderAcceptDTO,
    OrderCourierUpdateDTO,
    OrderOperatorUpdateDTO,
    OrdersDTO,
    OrderDTO,
    OrderCreateInputDTO,
)
from src.core.application.use_cases.dtos.order_item_dtos import (
    OrderItemDTO,
    OrderItemCreateDTO,
    GetOrderItemsInputDTO,
    OrderItemsDTO
)

from src.core.application.use_cases.dtos.auth_dtos import TokenDataDTO

from src.core.application.use_cases.get_order_items_use_case import GetOrderItemsUseCase
from src.core.application.use_cases.get_orders_use_case import GetOrdersUseCase
from src.core.application.use_cases.post_order_use_case import PostOrderUseCase
from src.core.application.use_cases.put_order_use_case import PutOrderUseCase
from src.core.application.use_cases.get_order_use_case import GetOrderUseCase
from src.core.application.use_cases.patch_order_courier_use_case import PatchOrderCourierUseCase
from src.core.application.use_cases.patch_order_payment_use_case import PatchOrderPaymentUseCase
from src.core.application.use_cases.patch_order_status_use_case import PatchOrderStatusUseCase
from src.core.application.use_cases.patch_order_accept_use_case import PatchOrderAcceptUseCase
from src.core.application.use_cases.patch_order_operator_use_case import PatchOrderOperatorUseCase

from src.presentation.api.v1.dependencies.order_di import (
    get_orders_use_case_di,
    get_order_use_case_di,
    post_order_use_case_di,
    put_order_use_case_di,
    patch_order_courier_use_case_di,
    patch_order_payment_use_case_di,    
    patch_order_status_use_case_di,
    patch_order_accept_use_case_di,
    patch_order_operator_use_case_di,
)
from src.presentation.api.v1.dependencies.order_item_di import (
    get_order_items_use_case_di,
)

router = APIRouter(prefix="/orders", tags=["Orders & Order Items"])

'''
orders & order items (Заказы)
{ GET: /orders , role{admin, main_operator, operator, customer}, query_parameters{user_id, status, limit, offset} }
{ POST: /orders , role{customer}, query_parameters{} }
{ GET: /orders/{order_id} , role{Any}, query_parameters{} }
{ PATCH: /orders/{order_id} , role{admin, main_operator}, query_parameters{} }
{ GET: /{order_id}/items , role{admin, main_operator, operator, customer}, query_parameters{order_id, limit, offset} }
{PATCH: /orders/{order_id}/courier , role{admin, main_operator, operator}, query_parameters{courier_id}}
{PATCH: /orders/{order_id}/payment , role{admin, main_operator, operator}, query_parameters{payment_method}}
{PATCH: /orders/{order_id}/status , role{admin, main_operator, operator}, query_parameters{status}}
{PATCH: /orders/{order_id}/accept , role{admin, main_operator, operator}, query_parameters{is_accepted}}
'''

@router.get(
        "/", 
        dependencies=[Depends(PermissionChecker(Permission.GET_ORDERS))], 
        response_model=OrdersDTO)
async def get_orders(
    limit: int = 10,
    offset: int = 0,
    token_data: TokenDataDTO = Depends(get_token_data),
    use_case: GetOrdersUseCase = Depends(get_orders_use_case_di)
):
    print(token_data)
    get_orders_input_dto = GetOrdersInputDTO(
        limit=limit,
        offset=offset,
        current_user_id=token_data.user_id,
        current_user_role=token_data.user_role
    )
    return await use_case.execute(get_orders_input_dto)

@router.post(
        "/", 
        dependencies=[Depends(PermissionChecker(Permission.POST_ORDER))],
        response_model=OrderDTO
    )
async def post_order(
    order_dto: OrderCreateInputDTO,
    token_data_dto: TokenDataDTO = Depends(get_token_data),
    use_case: PostOrderUseCase = Depends(post_order_use_case_di)
):
    create_order_dto = OrderCreateDTO(
        current_user_id=token_data_dto.user_id,
        current_user_role=token_data_dto.user_role,
        **order_dto.model_dump()
    )
    return await use_case.execute(create_order_dto)

@router.get(
        "/{order_id}", 
        dependencies=[Depends(PermissionChecker(Permission.GET_ORDER))],
        response_model=OrderDTO
    )
async def get_order(
    order_id: int,
    token_data_dto: TokenDataDTO = Depends(get_token_data),
    use_case: GetOrderUseCase = Depends(get_order_use_case_di)
):
    try:
        get_order_input_dto = GetOrderInputDTO(
            id=order_id,
            current_user_id=token_data_dto.user_id,
            current_user_role=token_data_dto.user_role
        )

        return await use_case.execute(get_order_input_dto)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

@router.put(
        "/{order_id}", 
        dependencies=[Depends(PermissionChecker(Permission.UPDATE_ORDER))],
        response_model=OrderDTO
    )
async def put_order(
    order_id: int,
    request_body: OrderUpdateRequest,
    token_data: TokenDataDTO = Depends(get_token_data),
    use_case: PutOrderUseCase = Depends(put_order_use_case_di)
):
    input_dto = UpdateOrderInputDTO(
        order_id=order_id,
        current_user_id=token_data.user_id,
        current_user_role=token_data.user_role,
        **request_body.model_dump()
    )
    return await use_case.execute(input_dto)

@router.get(
        "/{order_id}/items", 
        dependencies=[Depends(PermissionChecker(Permission.GET_ORDER_ITEMS))],
        response_model=OrderItemsDTO
    )
async def get_order_items(
    order_id: int,
    limit: int = 10,
    offset: int = 0,
    token_data: TokenDataDTO = Depends(get_token_data),
    use_case: GetOrderItemsUseCase = Depends(get_order_items_use_case_di)
):
    get_order_items_input_dto = GetOrderItemsInputDTO(
        order_id=order_id,
        limit=limit,
        offset=offset,
        current_user_id=token_data.user_id,
        current_user_role=token_data.user_role
    )
    
    return await use_case.execute(get_order_items_input_dto)

@router.patch(
        "/{id}/courier", 
        dependencies=[Depends(PermissionChecker(Permission.UPDATE_ORDER))],
        response_model=OrderDTO,
)
async def patch_order_courier(
    id: int,
    courier_id: int,
    token_data: TokenDataDTO = Depends(get_token_data),
    use_case: PatchOrderCourierUseCase = Depends(patch_order_courier_use_case_di)
):
    
    order_courier_update_dto = OrderCourierUpdateDTO(
        courier_id=courier_id,
        order_id=id,
    )

    return await use_case.execute(order_courier_update_dto)

@router.patch(
        "/{order_id}/operator", 
        dependencies=[Depends(PermissionChecker(Permission.GET_ORDER))],
        response_model=OrderDTO
        )
async def patch_order_operator(
    order_id: int,
    operator_id: int,
    token_data: TokenDataDTO = Depends(get_token_data),
    use_case: PatchOrderOperatorUseCase = Depends(patch_order_operator_use_case_di)
):
    order_operator_update_dto = OrderOperatorUpdateDTO(
        operator_id=operator_id,
        order_id=order_id,
    )
    return await use_case.execute(order_operator_update_dto)


@router.patch(
        "/{order_id}/payment", 
        dependencies=[Depends(PermissionChecker(Permission.UPDATE_ORDER))],
        response_model=OrderDTO
    )
async def patch_order_payment(
    order_id: int,
    payment_method: OrderPaymentMethodDTO,
    token_data: TokenDataDTO = Depends(get_token_data),
    use_case: PatchOrderPaymentUseCase = Depends(patch_order_payment_use_case_di)
):
    order_payment_input_dto = OrderPaymentUpdateDTO(
        order_id=order_id,
        current_user_id=token_data.user_id,
        current_user_role=token_data.user_role,
        payment_method=payment_method.payment_method
    )
    return await use_case.execute(order_payment_input_dto)

@router.patch(
        "/{order_id}/status", 
        dependencies=[Depends(PermissionChecker(Permission.UPDATE_ORDER))],
        response_model=OrderDTO
    )
async def patch_order_status(
    order_id: int,
    status: OrderStatusDTO,
    token_data: TokenDataDTO = Depends(get_token_data),
    use_case: PatchOrderStatusUseCase = Depends(patch_order_status_use_case_di)
):
    input_dto = OrderStatusUpdateDTO(
        order_id=order_id,
        current_user_id=token_data.user_id,
        current_user_role=token_data.user_role,
        status=status.status
    )
    return await use_case.execute(input_dto)


# {PATCH: /orders/{order_id}/accept , role{admin, main_operator, operator}, query_parameters{is_accepted}}
@router.patch(
        "/{order_id}/accept", 
        dependencies=[Depends(PermissionChecker(Permission.UPDATE_ORDER))],
        response_model=OrderDTO
    )
async def patch_order_accept(
    order_id: int,
    is_accepted: OrderAcceptDTO,
    token_data: TokenDataDTO = Depends(get_token_data),
    use_case: PatchOrderAcceptUseCase = Depends(patch_order_accept_use_case_di)
):    
    input_dto = OrderAcceptUpdateDTO(
        order_id=order_id,
        current_user_id=token_data.user_id,
        current_user_role=token_data.user_role,
        is_accepted=is_accepted.is_accepted
    )
    return await use_case.execute(input_dto)
