
class AdminDashboardDTO:
    def __init__(self, user_id: int):
        self.user_id = user_id


class AdminDashboardResponseDTO:
    def __init__(self, users_count: int, active_orders: int, revenue_today: float):
        self.users_count = users_count
        self.active_orders = active_orders
        self.revenue_today = revenue_today
