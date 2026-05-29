from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.models.user import User as UserModel

class UserDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user: UserModel) -> UserModel:
        self.session.add(instance=user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def count_all(self) -> int:
        result = await self.session.execute(select(func.count(UserModel.id)))
        return result.scalar() or 0
    
    async def get_by_id(self, user_id: int) -> UserModel | None:
        return await self.session.get(UserModel, user_id)
    
    async def get_by_telegram_id(self, telegram_id: int) -> UserModel | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> UserModel | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        return result.scalar_one_or_none()
    
    async def update(self, user: UserModel) -> UserModel:
        result = await self.session.execute(
            update(UserModel)
            .where(UserModel.id == user.id)
            .values(
                telegram_id=user.telegram_id,
                first_name=user.first_name,
                username=user.username,
                hashed_pwd=user.hashed_pwd,
                role=user.role,
                branch_id=user.branch_id,
            )
            .returning(UserModel)
        )
        obj = result.scalar_one()
        await self.session.commit()
        return obj

    async def delete(self, user_id: int) -> UserModel:
        result = await self.session.execute(
            delete(UserModel)
            .where(UserModel.id == user_id)
        )
        await self.session.commit()
        return result.rowcount > 0

    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[UserModel]:
        query = select(UserModel)
        
        if filters:
            query = query.filter_by(**filters)
        
        result = await self.session.execute(
            query.order_by(UserModel.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
        