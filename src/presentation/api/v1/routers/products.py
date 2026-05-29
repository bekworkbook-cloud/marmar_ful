from fastapi import APIRouter, Depends, File, UploadFile, status, Response, HTTPException, Query
from typing import Annotated

from src.presentation.api.v1.dependencies.ident_user_permissions_fd import PermissionChecker
from src.presentation.api.v1.dependencies.auth import check_token, get_token_data
from src.core.domain.enums.permissions import Permission
from src.core.application.use_cases.get_products_use_case import GetProductsUseCase
from src.core.application.use_cases.get_product_use_case import GetProductUseCase
from src.core.application.use_cases.post_product_use_case import PostProductUseCase
from src.core.application.use_cases.patch_product_use_case import PatchProductUseCase
from src.core.application.use_cases.delete_product_use_case import DeleteProductUseCase
from src.core.application.use_cases.put_product_use_case import PutProductUseCase
from src.core.application.use_cases.upload_product_image_use_case import UploadProductImageUseCase

from src.presentation.api.v1.dependencies.product_di import (
    get_products_use_case_di,
    post_product_use_case_di,
    get_product_use_case_di,
    put_product_use_case_di,
    delete_product_use_case_di,
    upload_product_image_use_case_di,
)

from src.core.application.use_cases.dtos.auth_dtos import TokenDataDTO
from src.core.application.use_cases.dtos.product_dtos import (
    ProductDTO,
    GetProductsInputDTO,
    GetProductsDTO,
    GetProductDTO,
    GetProductInputDTO,
    ProductUpdateDTO,
    ProductUpdateInputDTO,
    ProductCreateDTO,
    ProductCreateInputDTO,
    ProductsDTO,
) 

router = APIRouter(prefix="/products", tags=["Products"])

'''
products (Товары)product_create_input
{ GET: /products , role{Any}, query_parameters{branch_id, category_id, limit, offset} }
{ POST: /products , role{admin}, query_parameters{} }
{ GET: /products/{product_id} , role{Any}, query_parameters{} }
{ PUT: /products/{product_id} , role{admin}, query_parameters{} }
{ DELETE: /products/{product_id} , role{admin}, query_parameters{} }
'''

@router.get(
        "/", 
        dependencies=[Depends(PermissionChecker(Permission.GET_PRODUCTS))],
        response_model=ProductsDTO
    )
async def get_products(
    # 👇 Заставляем FastAPI читать DTO из Query-параметров URL, а не из Body
    category_id: int = Query(None, description="Категория ID"),
    limit: int = Query(10, description="Количество записей в ответе"),
    offset: int = Query(0, description="Смещение в ответе"),
    token_data: TokenDataDTO = Depends(get_token_data),
    use_case: GetProductsUseCase = Depends(get_products_use_case_di)
):
    get_rpoduct_dto = GetProductsDTO(
        category_id=category_id,
        limit=limit,
        offset=offset,
        current_user_id=token_data.user_id,
        current_user_role=token_data.user_role
    )
    return await use_case.execute(get_rpoduct_dto)

@router.post(
        "/", 
        dependencies=[Depends(PermissionChecker(Permission.POST_PRODUCT))],
        response_model=ProductDTO
    )
async def post_product(
    product_create_input: ProductCreateInputDTO,
    token_data: TokenDataDTO = Depends(get_token_data),
    use_case: PostProductUseCase = Depends(post_product_use_case_di)
    ):
    product_update_dto = ProductCreateDTO(
        name=product_create_input.name,
        category_id=product_create_input.category_id,
        branch_id=product_create_input.branch_id,
        description=product_create_input.description,
        price=product_create_input.price,
        is_active=product_create_input.is_active,
        maintenance_day=product_create_input.maintenance_day,
        maintenance_night=product_create_input.maintenance_night,
        current_user_id=token_data.user_id,
        current_user_role=token_data.user_role
    )
    return await use_case.execute(product_update_dto)

@router.get(
        "/{product_id}", 
        dependencies=[Depends(PermissionChecker(Permission.GET_PRODUCT))],
        response_model=ProductDTO
    )
async def get_product(
    product_id: int,
    token_data: TokenDataDTO = Depends(get_token_data),
    use_case: GetProductUseCase = Depends(get_product_use_case_di)
    ):
    get_product_dto = GetProductDTO(
        product_id=product_id,
        current_user_id=token_data.user_id,
        current_user_role=token_data.user_role
    )
    return await use_case.execute(get_product_dto)


@router.put(
        "/{product_id}", 
        dependencies=[Depends(PermissionChecker(Permission.UPDATE_PRODUCT))],
        response_model=ProductDTO
)
async def put_product(
    product_id: int,
    product_upd: ProductUpdateInputDTO,
    token_data: TokenDataDTO = Depends(get_token_data),
    use_case: PutProductUseCase = Depends(put_product_use_case_di)
    ):

    product_update_dto = ProductUpdateDTO(
        product_id=product_id,
        name=product_upd.name,
        category_id=product_upd.category_id,
        branch_id=product_upd.branch_id,
        description=product_upd.description,
        price=product_upd.price,
        is_active=product_upd.is_active,
        current_user_id=token_data.user_id,
        current_user_role=token_data.user_role
    )

    return await use_case.execute(product_update_dto)



@router.delete(
        "/{product_id}", 
        status_code=status.HTTP_204_NO_CONTENT, 
        response_class=Response, 
        dependencies=[Depends(PermissionChecker(Permission.DELETE_PRODUCT))]
    )
async def delete_product(
    product_id: int,
    token: str = Depends(check_token),
    use_case: DeleteProductUseCase = Depends(delete_product_use_case_di)
) -> None:    
    is_deleted = await use_case.execute(product_id)
    
    if not is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден")


@router.post(
        
        "/{product_id}/image", 
        dependencies=[Depends(PermissionChecker(Permission.UPDATE_PRODUCT))],
        response_model=ProductDTO
    )
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    use_case: UploadProductImageUseCase = Depends(upload_product_image_use_case_di)
):
    return await use_case.execute(product_id=product_id, file=file)
