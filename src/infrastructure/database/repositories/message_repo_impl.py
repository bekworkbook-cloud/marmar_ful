from src.core.domain.interfaces.message_repo import MessageRepository
from src.core.domain.entities.message import Message
from src.infrastructure.database.models.message import Message as MessageModel
from src.infrastructure.database.dao.message_dao import MessageDAO

class MessageRepositoryImpl(MessageRepository):
    def __init__(self, message_dao: MessageDAO):
        self.message_dao = message_dao

    def _to_entity(self, model: MessageModel) -> Message:
        return Message(
            id=model.id,
            order_id=model.order_id,
            sender_id=model.sender_id,
            text=model.text,
            created_at=model.created_at
        )

    def _to_model(self, entity: Message) -> MessageModel:
        return MessageModel(
            id=entity.id,
            order_id=entity.order_id,
            sender_id=entity.sender_id,
            text=entity.text,
            created_at=entity.created_at
        )

    async def add(self, message: Message) -> Message:
        message_model = self._to_model(message)
        created_model = await self.message_dao.add(message_model)
        return self._to_entity(created_model)

    async def post_message(self, message: Message) -> Message:
        return await self.add(message)

    async def get_messages(self, order_id: int) -> list[Message]:
        models = await self.message_dao.get_by_order(order_id)
        return [self._to_entity(model) for model in models]

    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[Message]:
        models = await self.message_dao.get_list(limit=limit, offset=offset, **filters)
        return [self._to_entity(model) for model in models]

