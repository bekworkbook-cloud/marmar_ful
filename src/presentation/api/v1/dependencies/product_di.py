from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.domain.interfaces.product_repo import ProductRepository
from src.infrastructure.database.repositories.product_repo_impl import ProductRepositoryImpl
from src.infrastructure.database.dao.product_dao import ProductDAO
from src.presentation.api.v1.dependencies.dependencies import get_db_session

from src.core.application.use_cases.get_products_use_case import GetProductsUseCase
from src.core.application.use_cases.get_product_use_case import GetProductUseCase
from src.core.application.use_cases.post_product_use_case import PostProductUseCase
from src.core.application.use_cases.put_product_use_case import PutProductUseCase
from src.core.application.use_cases.patch_product_use_case import PatchProductUseCase
from src.core.application.use_cases.delete_product_use_case import DeleteProductUseCase
from src.core.application.use_cases.upload_product_image_use_case import UploadProductImageUseCase

from src.infrastructure.external_services.file_storage import IFileStorage, LocalFileStorage

def get_product_repo(session: AsyncSession = Depends(get_db_session)) -> ProductRepository:
    return ProductRepositoryImpl(product_dao = ProductDAO(session))

def get_products_use_case_di(repo: ProductRepository = Depends(get_product_repo)):
    return GetProductsUseCase(repo)

def post_product_use_case_di(repo: ProductRepository = Depends(get_product_repo)):
    return PostProductUseCase(repo)

def get_product_use_case_di(repo: ProductRepository = Depends(get_product_repo)):
    return GetProductUseCase(repo)

def put_product_use_case_di(repo: ProductRepository = Depends(get_product_repo)):
    return PutProductUseCase(repo)

def delete_product_use_case_di(repo: ProductRepository = Depends(get_product_repo)):
    return DeleteProductUseCase(repo)

def upload_product_image_use_case_di(
        product_repo: ProductRepository = Depends(get_product_repo),
        file_storage: IFileStorage = Depends(LocalFileStorage)
    ):
    return UploadProductImageUseCase(
        product_repo=product_repo,
        file_storage=file_storage
    )