from src.core.domain.interfaces.message_repo import MessageRepository
from src.core.domain.interfaces.order_repo import OrderRepository
from src.core.application.exceptions.not_found_exception import NotFoundException
from src.core.domain.entities.message import Message
from src.core.application.use_cases.dtos.message_dtos import MessageDTO, MessageCreateDTO

class PostMessageUseCase:
    def __init__(self, message_repo: MessageRepository, order_repo: OrderRepository):
        self.message_repo = message_repo
        self.order_repo = order_repo

    async def execute(self, message_create: MessageCreateDTO) -> MessageDTO:
        message_entity = Message(
            id=None,
            sender_id=message_create.current_user_id,
            order_id=message_create.order_id,
            text=message_create.text,
            created_at=None
        )

        order_entity = await self.order_repo.get_by_id(message_create.order_id)

        if order_entity is None:
            raise NotFoundException(f"Order with id {message_create.order_id} not found")

        if message_create.current_user_id not in [order_entity.customer_id, order_entity.operator_id, order_entity.courier_id]:
            raise NotFoundException(f"Order with id {message_create.order_id} not found")

        created_entity = await self.message_repo.add(message=message_entity)
        
        return MessageDTO(
            id=created_entity.id,
            sender_id=created_entity.sender_id,
            order_id=created_entity.order_id,
            text=created_entity.text,
            created_at=created_entity.created_at.isoformat()
        )
