from src.infrastructure.database.models.order_item import OrderItem

from src.infrastructure.database.dao.base import BaseDAO

class OrderItemDAO(BaseDAO):
    model = OrderItem

    