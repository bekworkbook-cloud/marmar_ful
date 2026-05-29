from src.core.domain.interfaces.order_repo import OrderRepository
from src.core.domain.interfaces.user_repo import UserRepository
from src.core.domain.enums.roles import UserRole
from src.core.application.use_cases.dtos.order_dtos import OrderDTO, GetOrdersInputDTO, OrdersDTO

class GetOrdersUseCase:
    def __init__(self, order_repo: OrderRepository, user_repo: UserRepository):
        self.order_repo = order_repo
        self.user_repo = user_repo
    
    async def execute(self, get_orders_input_dto: GetOrdersInputDTO) -> OrdersDTO:
        role = get_orders_input_dto.current_user_role
        user_id = get_orders_input_dto.current_user_id
        user_entity = await self.user_repo.get_by_id(user_id)


        if role == UserRole.CUSTOMER.value:
            order_entities = await self.order_repo.get_list(
                limit=get_orders_input_dto.limit,
                offset=get_orders_input_dto.offset,
                customer_id=user_id
            )
        elif role == UserRole.COURIER.value:
            order_entities = await self.order_repo.get_list(
                limit=get_orders_input_dto.limit,
                offset=get_orders_input_dto.offset,
                courier_id=user_id
            )
            order_entities += await self.order_repo.get_list(
                limit=get_orders_input_dto.limit,
                offset=get_orders_input_dto.offset,
                courier_id=None
            )
            
        elif role == UserRole.ADMIN.value:
            order_entities = await self.order_repo.get_list(
                limit=get_orders_input_dto.limit,
                offset=get_orders_input_dto.offset
            )
        elif role == UserRole.MAINOPERATOR.value:
            order_entities = await self.order_repo.get_list(
                limit=get_orders_input_dto.limit,
                offset=get_orders_input_dto.offset,
                branch_id=user_entity.branch_id
            )
        elif role in (UserRole.OPERATOR.value, UserRole.MAINOPERATOR.value):
            order_entities = await self.order_repo.get_list(
                limit=get_orders_input_dto.limit,
                offset=get_orders_input_dto.offset,
                operator_id=user_id
            )
            order_entities += await self.order_repo.get_list(
                limit=get_orders_input_dto.limit,
                offset=get_orders_input_dto.offset,
                operator_id=None
            )
            
        orders_dtos_list = [
            OrderDTO(
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
            for order in order_entities
        ]
        print(orders_dtos_list)
        return OrdersDTO(orders=orders_dtos_list)