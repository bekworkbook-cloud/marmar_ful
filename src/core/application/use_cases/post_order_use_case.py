from src.core.domain.enums.order_status import OrderStatus
from src.core.domain.interfaces.order_repo import OrderRepository
from src.core.domain.interfaces.order_item_repo import OrderItemRepository
from src.core.domain.interfaces.product_repo import ProductRepository
from src.core.domain.interfaces.user_repo import UserRepository
from src.core.domain.entities.order import Order
from src.core.domain.entities.order_item import OrderItem
from src.core.application.use_cases.dtos.order_dtos import OrderDTO, OrderCreateDTO

from src.presentation.bots.customer_bot.services.send_invoice_service import send_payment_invoice

class PostOrderUseCase:
    def __init__(
        self, 
        order_repo: OrderRepository, 
        order_item_repo: OrderItemRepository,
        product_repo: ProductRepository,
        user_repo: UserRepository
    ):
        self.order_repo = order_repo
        self.order_item_repo = order_item_repo
        self.product_repo = product_repo
        self.user_repo = user_repo

    async def execute(self, order_create: OrderCreateDTO) -> OrderDTO:
        calculated_items = []
        total_price = 0

        user = await self.user_repo.get_by_id(order_create.current_user_id)

        for item in order_create.order_items:
            product = await self.product_repo.get_by_id(item.product_id)
            current_price = product.price
            total_price += current_price * item.quantity
            
            calculated_items.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": current_price
            })

        order_entity = Order(
            id=None,
            customer_id=order_create.current_user_id,
            operator_id=None,
            courier_id=None,
            branch_id=order_create.branch_id,
            status=OrderStatus.PENDING.value,
            payment_method=order_create.payment_method,
            total_price=total_price,
            is_accepted=False,
            address=order_create.address,
            landmark=order_create.landmark,
            latitude=order_create.latitude,
            longitude=order_create.longitude
        )
        
        created_order = await self.order_repo.add(order=order_entity)
        
        for item_data in calculated_items:
            order_item_entity = OrderItem(
                id=None,
                order_id=created_order.id,
                product_id=item_data["product_id"],
                quantity=item_data["quantity"],
                price=item_data["price"]
            )
            await self.order_item_repo.add(order_item_entity)

        if created_order.payment_method == "click" or created_order.payment_method == "payme":
            await send_payment_invoice(
                chat_id=user.telegram_id,
                provider=created_order.payment_method,
                price=created_order.total_price,
                payload=f"order_id:{created_order.id}")

        return OrderDTO(
            id=created_order.id,
            customer_id=created_order.customer_id,
            operator_id=created_order.operator_id,
            courier_id=created_order.courier_id,
            branch_id=created_order.branch_id,
            status=created_order.status,
            payment_method=created_order.payment_method,
            total_price=created_order.total_price,
            is_accepted=created_order.is_accepted,
            address=created_order.address,
            landmark=created_order.landmark,
            latitude=created_order.latitude,
            longitude=created_order.longitude
        )