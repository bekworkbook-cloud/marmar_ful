from src.core.domain.interfaces.order_item_repo import OrderItemRepository
from src.core.application.use_cases.dtos.order_item_dtos import OrderItemDTO, OrderItemsDTO, GetOrderItemsInputDTO


class GetOrderItemsUseCase:
    def __init__(self, order_item_repo: OrderItemRepository):
        self.order_item_repo = order_item_repo
    
    async def execute(self, get_order_items_input_dto: GetOrderItemsInputDTO) -> OrderItemsDTO:
        order_id = get_order_items_input_dto.order_id
        limit = get_order_items_input_dto.limit 
        offset = get_order_items_input_dto.offset

        order_item_entities = await self.order_item_repo.get_list(
            limit=limit, 
            offset=offset,
            order_id=order_id, 
        )
            
        order_items_dtos_list = [
            OrderItemDTO(
                id=order_item.id,
                order_id=order_item.order_id,
                product_id=order_item.product_id,
                quantity=order_item.quantity,
                price_at_purchase=order_item.price
            )
            for order_item in order_item_entities
        ]

        return OrderItemsDTO(order_items=order_items_dtos_list)
    