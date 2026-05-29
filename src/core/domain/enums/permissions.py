import enum


class Permission(enum.Enum):
    '''Branches'''
    GET_BRANCHES = 'get_branches'
    POST_BRANCH = 'post_branch'
    GET_BRANCH = 'get_branch'
    UPDATE_BRANCH = 'update_branch'
    PATCH_BRANCH = 'patch_branch'
    DELETE_BRANCH = 'delete_branch'

    '''Categories'''
    GET_CATEGORIES = 'get_categories'
    POST_CATEGORY = 'post_category'
    GET_CATEGORY = 'get_category'
    UPDATE_CATEGORY = 'update_category'
    DELETE_CATEGORY = 'delete_category'

    '''Products'''
    GET_PRODUCTS = 'get_products'
    GET_PRODUCT = 'get_product'
    POST_PRODUCT = 'post_product'
    UPDATE_PRODUCT = 'update_product'
    DELETE_PRODUCT = 'delete_product'

    '''Orders & order items'''
    GET_ORDERS = 'get_orders'
    GET_ORDER = 'get_order'
    POST_ORDER = 'post_order'
    UPDATE_ORDER = 'update_order'
    GET_ORDER_ITEMS = 'get_order_itmes'

    '''Messages'''
    GET_MESSAGES = 'get_messages'
    POST_MESSAGES = 'post_messges'

    '''Payment logs'''
    GET_PAYMENT_LOGS = 'get_payment_logs'
    POST_PAYMENT_LOGS = 'post_payment_logs'
    UPDATE_PAYMENT_LOGS = 'update_payment_logs'

    '''Users'''
    GET_USERS = 'get_users'
    POST_USERS = 'post_users'
    UPDATE_USERS = 'update_users'
    DELETE_USERS = 'delete_users'

    '''Auth'''
    POST_REGISTER = 'post_register'
    POST_LOGIN = 'post_login'
    DELETE_USER = 'delete_user'
    GET_ME = 'get_me'
    INIT_DATA = 'init_data'
