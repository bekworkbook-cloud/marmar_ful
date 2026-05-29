from src.core.domain.interfaces.order_repo import OrderRepository
from src.core.domain.interfaces.user_repo import UserRepository
from src.core.application.use_cases.dtos.order_dtos import OrderDTO, GetOrderInputDTO
from src.core.application.exceptions.auth import UnauthorizedError
from src.core.application.exceptions.not_found_exception import NotFoundException
from src.core.domain.enums.roles import UserRole

class GetOrderUseCase:
    def __init__(self, order_repo: OrderRepository, user_repo: UserRepository):
        self.order_repo = order_repo
        self.user_repo = user_repo

    async def execute(self, get_order_input_dto: GetOrderInputDTO) -> OrderDTO:
        order = await self.order_repo.get_by_id(order_id=get_order_input_dto.id)
        if not order:
            raise NotFoundException(f"Order with id {get_order_input_dto.id} not found")

        role = get_order_input_dto.current_user_role
        user_id = get_order_input_dto.current_user_id

        if user_id is not None:
            if role == UserRole.CUSTOMER.value:
                if order.customer_id != user_id:
                    raise UnauthorizedError("Forbidden: insufficient permissions")
            
            elif role == UserRole.COURIER.value:
                if order.courier_id and order.courier_id != user_id:
                    raise UnauthorizedError("Forbidden: insufficient permissions")
            
            elif role == UserRole.OPERATOR.value:
                if order.operator_id and order.operator_id != user_id:
                    raise UnauthorizedError("Forbidden: insufficient permissions")
            
            elif role == UserRole.MAINOPERATOR.value:
                user_entity = await self.user_repo.get_by_id(user_id)
                if order.branch_id and order.branch_id != user_entity.branch_id:
                    raise UnauthorizedError("Forbidden: insufficient permissions")
        
        return OrderDTO(
            id=order.id,
            customer_id=order.customer_id,
            operator_id=order.operator_id,
            courier_id=order.courier_id,
            branch_id=order.branch_id,
            status=order.status,
            payment_method=order.payment_method,
            total_price=order.total_price,
            is_accepted=order.is_accepted,
            address=order.address,
            landmark=order.landmark,
            latitude=order.latitude,
            longitude=order.longitude
        )
    