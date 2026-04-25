from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from src.infrastructure.database.models.user import User as UserModel

class UserDAO:
    def __init__(self, session):
        self.session = session

    async def count_all(self) -> int:
        result = await self.session.execute(select(func.count(UserModel.id)))
        # scalar() возвращает число, а не объект корутины или Row
        return result.scalar() or 0
    
    async def get_by_id(self, user_id: int):
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_telegram_id(self, telegram_id: int):
        result = await self.session.execute(
            select(UserModel).where(UserModel.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()
    

    
