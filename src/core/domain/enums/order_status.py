import enum


class OrderStatus(enum.Enum):
    CART = "корзина"
    PENDING = "ожидает оплаты"
    AWAITING_CONFIRMATION = "ожидает подтверждения"
    CONFIRMED = "подтвержден"
    PREPARING = "готовится"
    DELIVERING = "в пути"
    DELIVERED = "доставлен"
    CANCELLED = "отменен"
    CLOSED = "закрыт"

