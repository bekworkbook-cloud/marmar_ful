import pytest

from src.core.domain.entities.user import User
from src.core.domain.enums.roles import UserRole
from src.core.domain.services.access_control import ROLE_PERMISSIONS
from src.core.domain.enums.permissions import Permission

def test_user_initialisation_customer():
    user = User(
        id=1,
        telegram_id=1234567,
        first_name="Andrey",
        username="alyosha",
        hashed_pwd="hashedpwdfortests",
        role=UserRole.CUSTOMER,
        branch_id=None,
        permissions=ROLE_PERMISSIONS.get(UserRole.CUSTOMER)
    )
    can_create_order = user.has_permission(Permission.POST_ORDER)
    can_access_to_chat = user.has_permission(Permission.GET_MESSAGES)
    can_delete_branch = user.has_permission(Permission.DELETE_BRANCH)


    assert user.id == 1
    assert user.telegram_id == 1234567
    assert user.first_name == "Andrey"
    assert user.username == "alyosha"
    assert user.hashed_pwd == "hashedpwdfortests"
    assert user.branch_id == None
    assert user.role == UserRole.CUSTOMER
    assert user.permissions == ROLE_PERMISSIONS.get(UserRole.CUSTOMER)
    
    assert can_access_to_chat == True
    assert can_create_order == True
    assert can_delete_branch == False


def test_user_initialisation_admin():
    user = User(
        id=23,
        telegram_id=1234567,
        first_name="Andrey",
        username="alyosha",
        hashed_pwd="hashedpwdfortests",
        role=UserRole.ADMIN,
        branch_id=2,
        permissions=ROLE_PERMISSIONS.get(UserRole.ADMIN)
    )


    assert user.id == 23
    assert user.telegram_id == 1234567
    assert user.first_name == "Andrey"
    assert user.username == "alyosha"
    assert user.hashed_pwd == "hashedpwdfortests"
    assert user.branch_id == 2
    assert user.role == UserRole.ADMIN
    assert user.permissions == ROLE_PERMISSIONS.get(UserRole.ADMIN)
    
    assert user.has_permission(Permission.GET_BRANCHES) == True
    assert user.has_permission(Permission.POST_BRANCH) == True
    assert user.has_permission(Permission.GET_BRANCH) == True
    assert user.has_permission(Permission.UPDATE_BRANCH) == True
    assert user.has_permission(Permission.DELETE_BRANCH) == True
    
    assert user.has_permission(Permission.GET_CATEGORIES) == True
    assert user.has_permission(Permission.POST_CATEGORY) == True
    assert user.has_permission(Permission.GET_CATEGORY) == True
    assert user.has_permission(Permission.UPDATE_CATEGORY) == True
    assert user.has_permission(Permission.DELETE_CATEGORY) == True
    
    assert user.has_permission(Permission.GET_PRODUCTS) == True
    assert user.has_permission(Permission.GET_PRODUCT) == True
    assert user.has_permission(Permission.POST_PRODUCT) == True
    assert user.has_permission(Permission.UPDATE_PRODUCT) == True
    assert user.has_permission(Permission.DELETE_PRODUCT) == True
    
    assert user.has_permission(Permission.GET_ORDERS) == True
    assert user.has_permission(Permission.GET_ORDER) == True
    assert user.has_permission(Permission.UPDATE_ORDER) == True
    assert user.has_permission(Permission.GET_ORDER_ITEMS) == True
    
    assert user.has_permission(Permission.GET_MESSAGES) == True
    assert user.has_permission(Permission.POST_MESSAGES) == False
    
    assert user.has_permission(Permission.GET_PAYMENT_LOGS) == True
    assert user.has_permission(Permission.UPDATE_PAYMENT_LOGS) == True
    
    assert user.has_permission(Permission.GET_USERS) == True
    assert user.has_permission(Permission.POST_USERS) == True
    assert user.has_permission(Permission.UPDATE_USERS) == True
    assert user.has_permission(Permission.DELETE_USERS) == True
    
    assert user.has_permission(Permission.GET_ME) == True
    assert user.has_permission(Permission.DELETE_USER) == True
