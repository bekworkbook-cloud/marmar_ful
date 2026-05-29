from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.models.payment_log import PaymentLog as PaymentLogModel

class PaymentLogDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, payment_log: PaymentLogModel) -> PaymentLogModel:
        self.session.add(instance=payment_log)
        await self.session.commit()
        await self.session.refresh(payment_log)
        return payment_log

    async def get_by_id(self, payment_log_id: int) -> PaymentLogModel | None:
        result = await self.session.execute(
            select(PaymentLogModel).where(PaymentLogModel.id == payment_log_id)
        )
        return result.scalar_one_or_none()

    async def get_by_order_id(self, order_id: int, branch_id: int, courier_id: int) -> list[PaymentLogModel]:
        result = await self.session.execute(
            select(PaymentLogModel).where(
                PaymentLogModel.order_id == order_id,
                PaymentLogModel.branch_id == branch_id,
                PaymentLogModel.courier_id == courier_id
            )
        )
        return list(result.scalars().all())

    async def update(self, payment_log: PaymentLogModel) -> PaymentLogModel:
        result = await self.session.execute(
            update(PaymentLogModel)
            .where(PaymentLogModel.id == payment_log.id)
            .values(
                order_id=payment_log.order_id,
                branch_id=payment_log.branch_id,
                courier_id=payment_log.courier_id,
                amount=payment_log.amount,
                status=payment_log.status,
            )
            .returning(PaymentLogModel)
        )
        obj = result.scalar_one()
        await self.session.commit()
        return obj

    async def delete(self, payment_log_id: int) -> PaymentLogModel:
        result = await self.session.execute(
            delete(PaymentLogModel)
            .where(PaymentLogModel.id == payment_log_id)
            .returning(PaymentLogModel)
        )
        obj = result.scalar_one()
        await self.session.commit()
        return obj

    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[PaymentLogModel]:
        query = select(PaymentLogModel)
        
        if filters:
            query = query.filter_by(**filters)
        
        result = await self.session.execute(
            query.order_by(PaymentLogModel.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())