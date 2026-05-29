from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.models.message import Message as MessageModel

class MessageDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, message: MessageModel) -> MessageModel:
        self.session.add(instance=message)
        await self.session.commit()
        await self.session.refresh(message)
        return message
    
    async def get_by_order(self, order_id: int) -> list[MessageModel]:
        result = await self.session.execute(
            select(MessageModel).where(MessageModel.order_id == order_id)
        )
        return list(result.scalars().all())
    
    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[MessageModel]:
        query = select(MessageModel)
        
        if filters:
            query = query.filter_by(**filters)
        
        result = await self.session.execute(
            query.order_by(MessageModel.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())