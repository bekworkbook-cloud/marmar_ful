from sqlalchemy import select
from src.core.domain.entities.chat_message import ChatMessage
from src.infrastructure.database.models.chat_message import ChatMessageModel

class MessageRepositoryImpl:
    def __init__(self, dao):
        self.dao = dao

    async def save(self, message: ChatMessage) -> ChatMessage:
        model = ChatMessageModel(
            sender_id=message.sender_id,
            recipient_id=message.recipient_id,
            order_id=message.order_id,
            text=message.text
        )
        self.dao.session.add(model)
        await self.dao.session.flush()
        message.id = model.id
        message.created_at = model.created_at
        return message

    async def get_history_by_order(self, order_id: int) -> list[ChatMessage]:
        stmt = (
            select(ChatMessageModel)
            .where(ChatMessageModel.order_id == order_id)
            .order_by(ChatMessageModel.created_at.asc())
        )
        result = await self.dao.session.execute(stmt)
        models = result.scalars().all()
        
        return [
            ChatMessage(
                id=m.id,
                sender_id=m.sender_id,
                recipient_id=m.recipient_id,
                order_id=m.order_id,
                text=m.text,
                created_at=m.created_at
            )
            for m in models
        ]