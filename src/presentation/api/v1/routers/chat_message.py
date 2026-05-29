from fastapi import APIRouter, Depends

from src.core.domain.enums.permissions import Permission
from src.presentation.api.v1.dependencies.ident_user_permissions_fd import PermissionChecker

from src.presentation.api.v1.dependencies.auth import check_token, get_token_data
from src.core.application.use_cases.get_messages_use_case import GetMessagesUseCase
from src.core.application.use_cases.post_message_use_case import PostMessageUseCase
from src.presentation.api.v1.dependencies.message_di import (
    get_messages_use_case_di,
    post_message_use_case_di,
)
from src.core.application.use_cases.dtos.message_dtos import (
    MessageCreateDTO,
    GetMessagesInputDTO,
    MessagePostDTO,
    MessagesDTO,
    MessageDTO,
)
from src.core.application.use_cases.dtos.auth_dtos import TokenDataDTO
from src.core.application.use_cases.dtos.order_dtos import OrderIdDTO


router = APIRouter(prefix="/orders", tags=["Messages"])

'''
messages (Чат по заказу)
{ GET: /orders/{order_id}/messages , role{admin, customer, courier}, query_parameters{limit, offset} }
{ POST: /orders/{order_id}/messages , role{customer, courier}, query_parameters{} }
'''


@router.get(
        "/{order_id}/messages", 
        dependencies=[Depends(PermissionChecker(Permission.GET_MESSAGES))],
        response_model=MessagesDTO
    )
async def get_messages(
    order_id: int,
    limit: int = 10,
    offset: int = 0,
    token_data: TokenDataDTO = Depends(get_token_data),
    use_case: GetMessagesUseCase = Depends(get_messages_use_case_di)
):
    input_dto = GetMessagesInputDTO(
        order_id=order_id,
        limit=limit,
        offset=offset,
        current_user_id=token_data.user_id,
        current_user_role=token_data.user_role
        )
    return await use_case.execute(input_dto)

@router.post(
        "/{order_id}/messages", 
        dependencies=[Depends(PermissionChecker(Permission.POST_MESSAGES))],
        response_model=MessageDTO
    )
async def post_message(
    order_id: int,
    message: MessagePostDTO,
    token_data: TokenDataDTO = Depends(get_token_data),
    use_case: PostMessageUseCase = Depends(post_message_use_case_di)
):
    sended_message_dto = MessageCreateDTO(
        text=message.text,
        current_user_id=token_data.user_id,
        current_user_role=token_data.user_role,
        order_id=order_id)
    
    return await use_case.execute(sended_message_dto)