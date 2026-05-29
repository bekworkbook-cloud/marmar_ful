from fastapi import APIRouter, Depends, Query, HTTPException, status, Response

from src.presentation.api.v1.dependencies.auth import check_token, get_token_data
from src.core.application.use_cases.dtos.auth_dtos import TokenDataDTO
from src.core.domain.enums.permissions import Permission

from src.core.application.use_cases.get_categories_by_branch_id_use_case import GetCategoriesByBranchIdUseCase
from src.core.application.use_cases.get_category_use_case import GetCategoryUseCase
from src.core.application.use_cases.post_category_use_case import PostCategoryUseCase
from src.core.application.use_cases.put_category_use_case import PutCategoryUseCase
from src.core.application.use_cases.delete_category_use_case import DeleteCategoryUseCase

from src.presentation.api.v1.dependencies.ident_user_permissions_fd import PermissionChecker
from src.presentation.api.v1.dependencies.category_di import (
    get_categories_use_case_di,
    post_category_di,
    get_category_use_case_di,
    patch_category_di,
    delete_category_di,
)
from src.core.application.use_cases.dtos.category_dtos import (
    CategoryIdDTO,
    CategoryCreateDTO,
    GetCategoryInputDTO,
    CategoryUpdateDTO,
    CategoriesDTO,
    CategoryDTO,

)

router = APIRouter(prefix="/categories", tags=["Categories"])

'''
categories (Категории)
{ GET: /categories , role{Any}, query_parameters{branch_id, limit, offset} }
{ POST: /categories , role{admin}, query_parameters{} }
{ GET: /categories/{category_id} , role{Any}, query_parameters{} }
{ PATCH: /categories/{category_id} , role{admin}, query_parameters{} }
{ DELETE: /categories/{category_id} , role{admin}, query_parameters{} }
'''

@router.get(
        "/",
        dependencies=[Depends(PermissionChecker(Permission.GET_CATEGORIES))],
        response_model=CategoriesDTO
    )
async def get_categories(
    branch_id: int = Query(..., description="Филиал ID"),
    limit: int = Query(10, description="Количество записей в ответе"),
    offset: int = Query(0, description="Смещение в ответе"),
    token: TokenDataDTO = Depends(check_token),
    use_case: GetCategoriesByBranchIdUseCase = Depends(get_categories_use_case_di)
    ):
    get_categories_input_dto = GetCategoryInputDTO(branch_id=branch_id, limit=limit, offset=offset)
    return await use_case.execute(get_categories_input_dto)


@router.post(
        "/", 
        dependencies=[Depends(PermissionChecker(Permission.POST_CATEGORY))],
        response_model=CategoryDTO
    )
async def post_categories(
    category_data: CategoryCreateDTO,
    token: TokenDataDTO = Depends(check_token),
    use_case: PostCategoryUseCase = Depends(post_category_di)
    ):
    return await use_case.execute(category_data)


@router.get(
        "/{category_id}", 
        dependencies=[Depends(PermissionChecker(Permission.GET_CATEGORY))],
        response_model=CategoryDTO,
    )
async def get_category(
    category_id: int,
    token: TokenDataDTO = Depends(check_token),
    use_case: GetCategoryUseCase = Depends(get_category_use_case_di)
    ):
    category_id_dto = CategoryIdDTO(id=category_id)
    return await use_case.execute(category_id_dto)


@router.put(
        "/{category_id}",
        dependencies=[Depends(PermissionChecker(Permission.UPDATE_CATEGORY))],
        response_model=CategoryDTO
    )
async def patch_category(
    category_id: int,
    category_data: CategoryUpdateDTO,
    token: TokenDataDTO = Depends(check_token),
    use_case: PutCategoryUseCase = Depends(patch_category_di)
    ):
    category_id_dto = CategoryIdDTO(id=category_id)
    return await use_case.execute(category_id_dto, category_data)

@router.delete(
        "/{category_id}", 
        dependencies=[Depends(PermissionChecker(Permission.DELETE_CATEGORY))],
        status_code=status.HTTP_204_NO_CONTENT, 
        response_class=Response, 
    )
async def delete_category(
    category_id: int,
    token: TokenDataDTO = Depends(check_token),
    use_case: DeleteCategoryUseCase = Depends(delete_category_di)
    ):
    category_id_dto = CategoryIdDTO(id=category_id)
    is_deleted = await use_case.execute(category_id_dto)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return HTTPException(status_code=204, detail="Категория успешно удалена")

