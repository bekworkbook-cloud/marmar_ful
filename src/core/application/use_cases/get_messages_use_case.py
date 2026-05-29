from src.core.domain.interfaces.message_repo import MessageRepository
from src.core.domain.interfaces.order_repo import OrderRepository
from src.core.application.use_cases.dtos.message_dtos import MessageDTO, MessagesDTO, GetMessagesInputDTO
from src.core.application.exceptions.not_found_exception import NotFoundException

class GetMessagesUseCase:
    def __init__(self, message_repo: MessageRepository, order_repo: OrderRepository):
        self.message_repo = message_repo
        self.order_repo = order_repo

    async def execute(self, input_dto: GetMessagesInputDTO) -> MessagesDTO:
        order_id = input_dto.order_id
        limit = input_dto.limit
        offset = input_dto.offset
        order_entity = await self.order_repo.get_by_id(order_id)
        if order_entity is None:
            raise NotFoundException(f"Order with id {order_id} not found")
        
        print(input_dto.current_user_role!="admin")

        if input_dto.current_user_role != "admin" and input_dto.current_user_id not in [order_entity.customer_id, order_entity.operator_id, order_entity.courier_id]:
            raise NotFoundException(f"Order with id {order_id} not found")

            
        messages_entities = await self.message_repo.get_list(order_id=order_id, limit=limit, offset=offset)
        messages_dtos_list = [
            MessageDTO(
                id=message.id,
                sender_id=message.sender_id,
                order_id=message.order_id,
                text=message.text,
                created_at=message.created_at.isoformat()
            )
            for message in messages_entities
        ]
        return MessagesDTO(messages=messages_dtos_list)
