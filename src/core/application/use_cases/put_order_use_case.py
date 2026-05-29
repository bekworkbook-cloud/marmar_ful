from src.core.domain.interfaces.order_repo import OrderRepository
from src.core.application.use_cases.dtos.order_dtos import OrderDTO, UpdateOrderInputDTO
from src.core.application.exceptions.not_found_exception import NotFoundException

class PutOrderUseCase:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo
    
    async def execute(self, input_dto: UpdateOrderInputDTO) -> OrderDTO:
        order_entity = await self.order_repo.get_by_id(order_id=input_dto.order_id)
        if not order_entity:
            raise NotFoundException(f"Order with id {input_dto.order_id} not found")
        
        order_entity.change_branch(branch_id=input_dto.branch_id)
        order_entity.update_payment_info(
            payment_method=input_dto.payment_method,
            is_accepted=input_dto.is_accepted
        )
        order_entity.correct_delivery_address(
            address=input_dto.address,
            landmark=input_dto.landmark,
            latitude=input_dto.latitude,
            longitude=input_dto.longitude
        )
        
        updated_entity = await self.order_repo.update(order_entity)
        
        return OrderDTO(
            id=updated_entity.id,
            customer_id=updated_entity.customer_id,
            operator_id=updated_entity.operator_id,
            courier_id=updated_entity.courier_id,
            branch_id=updated_entity.branch_id,
            status=updated_entity.status,
            payment_method=updated_entity.payment_method,
            total_price=updated_entity.total_price,
            is_accepted=updated_entity.is_accepted,
            address=updated_entity.address,
            landmark=updated_entity.landmark,
            latitude=updated_entity.latitude,
            longitude=updated_entity.longitude
        )