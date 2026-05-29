from src.core.domain.interfaces.payment_log_repo import PaymentLogRepository
from src.core.domain.entities.payment import PaymentLog
from src.infrastructure.database.models.payment_log import PaymentLog as PaymentLogModel
from src.infrastructure.database.dao.payment_log_dao import PaymentLogDAO

class PaymentLogRepositoryImpl(PaymentLogRepository):
    def __init__(self, payment_log_dao: PaymentLogDAO):
        self.payment_log_dao = payment_log_dao

    def _to_entity(self, model: PaymentLogModel) -> PaymentLog:
        return PaymentLog(
            id=model.id,
            order_id=model.order_id,
            branch_id=model.branch_id,
            courier_id=model.courier_id,
            amount=model.amount,
            status=model.status,
            created_at=model.created_at
        )

    def _to_model(self, entity: PaymentLog) -> PaymentLogModel:
        return PaymentLogModel(
            id=entity.id,
            order_id=entity.order_id,
            branch_id=entity.branch_id,
            courier_id=entity.courier_id,
            amount=entity.amount,
            status=entity.status,
            created_at=entity.created_at
        )

    async def add(self, payment_log: PaymentLog) -> PaymentLog:
        model = self._to_model(payment_log)
        created_model = await self.payment_log_dao.add(model)
        return self._to_entity(created_model)

    async def get_by_id(self, payment_log_id: int) -> PaymentLog:
        model = await self.payment_log_dao.get_by_id(payment_log_id)
        return self._to_entity(model)
    
    async def get_by_order_id(self, order_id: int, branch_id: int, courier_id: int) -> list[PaymentLog]:
        models = await self.payment_log_dao.get_by_order_id(
            order_id=order_id, 
            branch_id=branch_id, 
            courier_id=courier_id
        )
        return [self._to_entity(model) for model in models]
    
    async def update(self, payment_log: PaymentLog) -> PaymentLog:
        model = self._to_model(payment_log)
        updated_model = await self.payment_log_dao.update(model)
        return self._to_entity(updated_model)
    
    async def delete(self, payment_log_id: int) -> None:
        await self.payment_log_dao.delete(payment_log_id)

    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[PaymentLog]:
        models = await self.payment_log_dao.get_list(limit=limit, offset=offset, **filters)
        return [self._to_entity(model) for model in models]