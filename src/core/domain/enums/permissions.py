import enum


class Permission(enum.Enum):
    ACCESS_OPERATOR_CHAT = "access_operator_chat"
    ACCESS_ADMIN_CHAT = "access_admin_chat"
    ACCESS_COURIER_CHAT = "access_courier_chat"
    ACCESS_CUSTOMER_CHAT = "access_customer_chat"

    CREATE_ORDER = "create_order"
    UPDATE_ORDER = "update_order"
    DELETE_ORDER = "delete_order"
    VIEW_ORDER = "view_order"

    CREATE_CATEGORY = "create_category"
    UPDATE_CATEGORY = "update_category"
    DELETE_CATEGORY = "delete_category"
    VIEW_CATEGORY = "view_category"

    CREATE_PRODUCT = "create_product"
    UPDATE_PRODUCT = "update_product"
    DELETE_PRODUCT = "delete_product"
    VIEW_PRODUCT = "view_porduct"

    VIEW_ADMIN_DASHBOARD = "view_admin_dashboard"
    VIEW_CUSTOMER_PAGE = "view_customer_page"

    ASSIGN_OPERATOR = "assign_operator"
    ASSIGN_MAIN_OPERATOR = "assign_main_operator"
    ASSIGN_COURIER = "assign_courier"

    CREATE_USER = "create_user"
    UPDATE_USER = "update_user"
    # delete нету потому что он одлжен остаться на базе.

    VIEW_ALL_ORDERS = "view_all_orders"

