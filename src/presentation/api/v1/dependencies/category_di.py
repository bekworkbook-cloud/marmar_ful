from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.domain.interfaces.category_repo import CategoryRepository
from src.infrastructure.database.repositories.category_repo_impl import CategoryRepositoryImpl
from src.infrastructure.database.dao.category_dao import CategoryDAO
from src.presentation.api.v1.dependencies.dependencies import get_db_session

from src.core.application.use_cases.get_category_use_case import GetCategoryUseCase
from src.core.application.use_cases.get_categories_by_branch_id_use_case import GetCategoriesByBranchIdUseCase
from src.core.application.use_cases.post_category_use_case import PostCategoryUseCase
from src.core.application.use_cases.put_category_use_case import PutCategoryUseCase
from src.core.application.use_cases.delete_category_use_case import DeleteCategoryUseCase

def get_category_repo(session: AsyncSession = Depends(get_db_session)) -> CategoryRepository:
    return CategoryRepositoryImpl(category_dao = CategoryDAO(session))

def get_categories_use_case_di(repo: CategoryRepository = Depends(get_category_repo)):
    return GetCategoriesByBranchIdUseCase(repo)

def post_category_di(repo: CategoryRepository = Depends(get_category_repo)):
    return PostCategoryUseCase(repo)

def get_category_use_case_di(repo: CategoryRepository = Depends(get_category_repo)):
    return GetCategoryUseCase(repo)

def patch_category_di(repo: CategoryRepository = Depends(get_category_repo)):
    return PutCategoryUseCase(repo)

def delete_category_di(repo: CategoryRepository = Depends(get_category_repo)):
    return DeleteCategoryUseCase(repo)