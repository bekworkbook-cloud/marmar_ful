import enum

class UserRole(enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    COURIER = "courier"
    OPERATOR = "operator"
    MAINOPERATOR = "main_operator"
    GUEST = "гость"
    # banned реализовать потом
