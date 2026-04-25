
class OrderService:

    def calculate_total(self, items):
        return sum(item.price * item.quantity for item in items)

    def can_be_cancelled(self, order):
        return order.status != "delivered"
