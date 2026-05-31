from fastapi import APIRouter, Depends, HTTPException, status, Response

from src.core.domain.enums.permissions import Permission
from src.core.application.use_cases.get_branches_use_case import GetBranchesUseCase
from src.core.application.use_cases.get_branch_use_case import GetBranchUseCase
from src.core.application.use_cases.delete_branches_use_case import DeleteBranchUseCase
from src.core.application.use_cases.put_branch_use_case import PutBranchUseCase
from src.core.application.use_cases.post_branches_use_case import PostBranchesUseCase

from src.core.application.use_cases.dtos.branch_dtos import (
    BranchDTO,
    DeleteBranchDTO,
    BranchCreateDTO,
    BranchesDTO,
    BranchIdDTO,
    BranchUpdateDTO
)

from src.presentation.api.v1.dependencies.auth import check_token, get_token_data
from src.presentation.api.v1.dependencies.branch_di import (
    get_branch_di,
    get_branches_di,
    delete_branch_di,
    put_branch_di,
    post_branch_di,
)
from src.presentation.api.v1.dependencies.ident_user_permissions_fd import PermissionChecker

router = APIRouter(prefix="/branches", tags=["Branches"])


@router.get(
    "/", 
    dependencies=[Depends(PermissionChecker(Permission.GET_BRANCHES))],
    response_model=BranchesDTO
)
async def get_branches(
    token: str = Depends(get_token_data),
    use_case: GetBranchesUseCase = Depends(get_branches_di)
):    
    branches = await use_case.execute()
    print(branches)
    return branches


@router.post(
    "/", 
    dependencies=[Depends(PermissionChecker(Permission.POST_BRANCH))],
    response_model=BranchDTO
)
async def post_branches(
    branch_create_dto: BranchCreateDTO,
    token_data_dto: str = Depends(get_token_data),
    use_case: PostBranchesUseCase = Depends(post_branch_di)
):    
    return await use_case.execute(branch_create_dto=branch_create_dto)


@router.get(
    "/{branch_id}", 
    dependencies=[Depends(PermissionChecker(Permission.GET_BRANCH))],
    response_model=BranchDTO
)
async def get_branch(
    branch_id: int,
    token: str = Depends(check_token),
    use_case: GetBranchUseCase = Depends(get_branch_di)
):
    branch_id_dto = BranchIdDTO(id=branch_id)
    return await use_case.execute(branch_id_dto=branch_id_dto)


@router.put(
    "/{branch_id}", 
    dependencies=[Depends(PermissionChecker(Permission.UPDATE_BRANCH))],
    response_model=BranchDTO
)
async def put_branch(
    branch_id: int,
    branch_update_dto: BranchUpdateDTO,
    token: str = Depends(check_token),
    use_case: PutBranchUseCase = Depends(put_branch_di)
):
    branch_id_dto = BranchIdDTO(id=branch_id)
    return await use_case.execute(branch_id=branch_id_dto, branch_update_dto=branch_update_dto)


@router.delete(
        "/{branch_id}", 
        status_code=status.HTTP_204_NO_CONTENT, 
        response_class=Response, 
        dependencies=[Depends(PermissionChecker(Permission.DELETE_BRANCH))]
    )
async def delete_branch(
    branch_id: int,
    token: str = Depends(check_token),
    use_case: DeleteBranchUseCase = Depends(delete_branch_di)
) -> None:
    delete_branch_dto = DeleteBranchDTO(id=branch_id)
    is_deleted = await use_case.execute(delete_branch_dto=delete_branch_dto)
    
    if not is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Филиал не найден")