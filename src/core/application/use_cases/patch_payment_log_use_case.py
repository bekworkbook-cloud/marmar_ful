from src.core.domain.interfaces.payment_log_repo import PaymentLogRepository
from src.core.application.use_cases.dtos.payment_log_dtos import PaymentLogDTO, PaymentLogIdDTO, PaymentLogUpdateDTO

class PatchPaymentLogUseCase:
    def __init__(self, payment_log_repo: PaymentLogRepository):
        self.payment_log_repo = payment_log_repo
    
    async def execute(self, payment_log_id: PaymentLogIdDTO, payment_log_update: PaymentLogUpdateDTO) -> PaymentLogDTO:
        payment_log_entity = await self.payment_log_repo.get_by_id(payment_log_id=payment_log_id.id)
        
        payment_log_entity.update_fields(
            order_id=payment_log_update.order_id,
            branch_id=payment_log_update.branch_id,
            courier_id=payment_log_update.courier_id,
            payment_method=payment_log_update.payment_method,
            amount=payment_log_update.amount,
            is_closed=payment_log_update.is_closed
        )
        
        updated_entity = await self.payment_log_repo.update(payment_log_entity)
        
        return PaymentLogDTO(
            id=updated_entity.id,
            order_id=updated_entity.order_id,
            branch_id=updated_entity.branch_id,
            courier_id=updated_entity.courier_id,
            payment_method=updated_entity.payment_method,
            amount=updated_entity.amount,
            is_closed=updated_entity.is_closed
        )