from src.core.domain.interfaces.payment_log_repo import PaymentLogRepository
from src.core.application.use_cases.dtos.payment_log_dtos import PaymentLogDTO, GetPaymentLogsInputDTO, PaymentLogsDTO

class GetPaymentLogsUseCase:
    def __init__(self, payment_log_repo: PaymentLogRepository):
        self.payment_log_repo = payment_log_repo
    
    async def execute(self, get_payment_logs_input_dto: GetPaymentLogsInputDTO) -> PaymentLogsDTO:
        order_id = get_payment_logs_input_dto.order_id
        branch_id = get_payment_logs_input_dto.branch_id
        courier_id = get_payment_logs_input_dto.courier_id
        limit = get_payment_logs_input_dto.limit
        offset = get_payment_logs_input_dto.offset
        
        payment_log_entities = await self.payment_log_repo.get_by_order_id(
            order_id=order_id,
            branch_id=branch_id,
            courier_id=courier_id,
            limit=limit,
            offset=offset
        )
        
        payment_logs_dtos_list = [
            PaymentLogDTO(
                id=payment_log.id,
                order_id=payment_log.order_id,
                branch_id=payment_log.branch_id,
                courier_id=payment_log.courier_id,
                payment_method=payment_log.payment_method,
                amount=payment_log.amount,
                is_closed=payment_log.is_closed
            )
            for payment_log in payment_log_entities
        ]
        return PaymentLogsDTO(payment_logs=payment_logs_dtos_list)