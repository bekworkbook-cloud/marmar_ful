from src.core.domain.interfaces.order_repo import OrderRepository
from src.core.application.use_cases.dtos.order_dtos import OrderDTO, OrderAcceptUpdateDTO
from src.core.application.exceptions.not_found_exception import NotFoundException


class PatchOrderAcceptUseCase:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo
    
    async def execute(self, create_order_input_dto: OrderAcceptUpdateDTO) -> OrderDTO:
        order_entity = await self.order_repo.get_by_id(order_id=create_order_input_dto.order_id)
        if not order_entity:
            raise NotFoundException(f"Order with id {create_order_input_dto.order_id} not found")
        
        order_entity.change_accept(is_accepted=create_order_input_dto.is_accepted)
        
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