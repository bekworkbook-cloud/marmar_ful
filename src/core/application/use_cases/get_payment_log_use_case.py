from src.core.domain.interfaces.payment_log_repo import PaymentLogRepository
from src.core.application.use_cases.dtos.payment_log_dtos import PaymentLogDTO, PaymentLogIdDTO

class GetPaymentLogUseCase:
    def __init__(self, payment_log_repo: PaymentLogRepository):
        self.payment_log_repo = payment_log_repo
    
    async def execute(self, payment_log_id_dto: PaymentLogIdDTO) -> PaymentLogDTO:        
        payment_log = await self.payment_log_repo.get_by_id(payment_log_id=payment_log_id_dto.id)
        return PaymentLogDTO(
            id=payment_log.id,
            order_id=payment_log.order_id,
            branch_id=payment_log.branch_id,
            courier_id=payment_log.courier_id,
            payment_method=payment_log.payment_method,
            amount=payment_log.amount,
            is_closed=payment_log.is_closed
        )