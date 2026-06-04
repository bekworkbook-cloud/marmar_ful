from fastapi import APIRouter, Depends, Response, status, HTTPException
from src.presentation.api.v1.dependencies.ident_user_permissions_fd import PermissionChecker
from src.presentation.api.v1.dependencies.auth import check_token
from src.core.domain.enums.permissions import Permission
from src.core.application.use_cases.get_users_use_case import GetUsersUseCase
from src.core.application.use_cases.get_user_use_case import GetUserUseCase
from src.core.application.use_cases.post_user_use_case import PostUserUseCase
from src.core.application.use_cases.patch_user_use_case import PatchUserUseCase
from src.core.application.use_cases.delete_user_use_case import DeleteUserUseCase
from src.core.application.use_cases.put_user_use_case import PutUserUseCase

from src.presentation.api.v1.dependencies.user_di import (
    get_users_use_case_di,
    get_user_use_case_di,
    post_user_use_case_di,
    patch_user_use_case_di,
    delete_user_use_case_di,
    put_user_use_case_di,
)    

from src.core.application.use_cases.dtos.user_dtos import (
    UserCreateDTO,
    GetUserInputDTO,
    GetUsersInputDTO,
    GetUserInputDTO,
    DeleteUserDTO,
)


router = APIRouter(prefix="/users", tags=["Users"])

'''
users (Пользователи)
{ GET: /users , role{admin}, query_parameters{role, search_query, limit, offset} }
{ POST: /users , role{admin}, query_parameters{} }
{ PATCH: /users/{user_id} , role{admin}, query_parameters{} }
{ DELETE: /users/{user_id} , role{admin}, query_parameters{} }
'''


@router.get("/", dependencies=[Depends(PermissionChecker(Permission.GET_USERS))])
async def get_users(
    role: str = None,
    branch_id: int = None,
    limit: int = 10,
    offset: int = 0,
    token: str = Depends(check_token),
    use_case: GetUsersUseCase = Depends(get_users_use_case_di)
    ):
    get_users_input_dto = GetUsersInputDTO(
        role=role, 
        branch_id=branch_id, 
        limit=limit, 
        offset=offset
    )
    users = await use_case.execute(get_users_input_dto=get_users_input_dto)
    print(users)
    return users


@router.get("/{user_id}", dependencies=[Depends(PermissionChecker(Permission.GET_USERS))])
async def get_user(
    user_id: int,
    token: str = Depends(check_token),
    use_case: GetUserUseCase = Depends(get_user_use_case_di)
):
    get_user_input_dto = GetUserInputDTO(
        user_id=user_id
    )
    return await use_case.execute(get_user_input_dto)


@router.post("/", dependencies=[Depends(PermissionChecker(Permission.POST_USERS))])
async def post_users(
    user: UserCreateDTO,
    token: str = Depends(check_token),
    use_case: PostUserUseCase = Depends(post_user_use_case_di)
    ):
    return await use_case.execute(user)

@router.put("/{user_id}", dependencies=[Depends(PermissionChecker(Permission.UPDATE_USERS))])
async def patch_user(
    user_id: int,
    user: UserCreateDTO,
    token: str = Depends(check_token),
    use_case: PutUserUseCase = Depends(put_user_use_case_di)
    ):
    return await use_case.execute(user_id, user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response, dependencies=[Depends(PermissionChecker(Permission.DELETE_USERS))])
async def delete_user(
    user_id: int,
    token: str = Depends(check_token),
    use_case: DeleteUserUseCase = Depends(delete_user_use_case_di)
    )-> None:
    delete_user_dto = DeleteUserDTO(user_id=user_id)
    is_deleted = await use_case.execute(delete_user_dto)

    if not is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
