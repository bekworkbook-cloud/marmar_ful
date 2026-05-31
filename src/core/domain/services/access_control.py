
from src.core.domain.enums.roles import UserRole
from src.core.domain.enums.permissions import Permission

ROLE_PERMISSIONS = {
    UserRole.CUSTOMER: {
        # Branches, Categories, Products (Role: Any)
        Permission.GET_BRANCHES,
        Permission.GET_BRANCH,
        Permission.GET_CATEGORIES,
        Permission.GET_CATEGORY,
        Permission.GET_PRODUCTS,
        Permission.GET_PRODUCT,
        # Orders & Items
        Permission.GET_ORDERS,       # Может видеть свои заказы
        Permission.POST_ORDER,
        Permission.GET_ORDER,
        Permission.GET_ORDER_ITEMS,
        # Messages
        Permission.GET_MESSAGES,
        Permission.POST_MESSAGES,
        # Auth
        Permission.GET_ME,
        Permission.DELETE_USER,
    },
    
    UserRole.COURIER: {
        # Branches, Categories, Products (Role: Any)
        Permission.GET_BRANCHES,
        Permission.GET_BRANCH,
        Permission.GET_CATEGORIES,
        Permission.GET_CATEGORY,
        Permission.GET_PRODUCTS,
        Permission.GET_PRODUCT,
        # Orders
        Permission.GET_ORDER,
        Permission.GET_ORDERS,       # Может видеть свои заказы
        Permission.UPDATE_ORDER,     # В схеме указано, что курьер может PATCH order
        Permission.GET_ORDER_ITEMS,
        Permission.POST_ORDER,
        # Messages
        Permission.GET_MESSAGES,
        Permission.POST_MESSAGES,
        # Auth
        Permission.GET_ME,
        Permission.DELETE_USER,
    },
    
    UserRole.OPERATOR: {
        
        Permission.GET_USERS,


        # Branches, Categories, Products (Role: Any)
        Permission.GET_BRANCHES,
        Permission.GET_BRANCH,
        Permission.GET_CATEGORIES,
        Permission.GET_CATEGORY,
        Permission.GET_PRODUCTS,
        Permission.GET_PRODUCT,
        # Orders
        Permission.GET_ORDERS,
        Permission.GET_ORDER,
        Permission.UPDATE_ORDER,
        Permission.GET_ORDER_ITEMS,
        Permission.POST_ORDER,
        # Messages
        Permission.GET_MESSAGES,
        Permission.POST_MESSAGES,
        # Auth
        Permission.GET_ME,
        Permission.DELETE_USER,
    },
    
    UserRole.MAINOPERATOR: {

        Permission.GET_USERS,

        # Все базовые права (Any)
        Permission.GET_BRANCHES,
        Permission.GET_BRANCH,
        Permission.GET_CATEGORIES,
        Permission.GET_CATEGORY,
        Permission.GET_PRODUCTS,
        Permission.GET_PRODUCT,
        # Orders
        Permission.GET_ORDERS,
        Permission.GET_ORDER,
        Permission.UPDATE_ORDER,
        Permission.GET_ORDER_ITEMS,
        Permission.POST_ORDER,
        # Payment Logs (admin, main_operator)
        Permission.GET_PAYMENT_LOGS,
        Permission.UPDATE_PAYMENT_LOGS,
        # Auth
        Permission.GET_ME,
        Permission.DELETE_USER,
        # Messages
        Permission.GET_MESSAGES,
        Permission.POST_MESSAGES,
    },
    
    UserRole.ADMIN: {
        # Branches
        Permission.GET_BRANCHES,
        Permission.POST_BRANCH,
        Permission.GET_BRANCH,
        Permission.UPDATE_BRANCH,
        Permission.DELETE_BRANCH,
        # Categories
        Permission.GET_CATEGORIES,
        Permission.POST_CATEGORY,
        Permission.GET_CATEGORY,
        Permission.UPDATE_CATEGORY,
        Permission.DELETE_CATEGORY,
        # Products
        Permission.GET_PRODUCTS,
        Permission.GET_PRODUCT,
        Permission.POST_PRODUCT,
        Permission.UPDATE_PRODUCT,
        Permission.DELETE_PRODUCT,
        # Orders & Items
        Permission.GET_ORDERS,
        Permission.GET_ORDER,
        Permission.UPDATE_ORDER,
        Permission.GET_ORDER_ITEMS,
        Permission.POST_ORDER,
        # Messages
        Permission.GET_MESSAGES,
        Permission.POST_MESSAGES,
        # Payment Logs
        Permission.GET_PAYMENT_LOGS,
        Permission.UPDATE_PAYMENT_LOGS,
        # Users
        Permission.GET_USERS,
        Permission.POST_USERS,
        Permission.UPDATE_USERS,
        Permission.DELETE_USERS,
        # Auth
        Permission.GET_ME,
        Permission.DELETE_USER,
    },
}