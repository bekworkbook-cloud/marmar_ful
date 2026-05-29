from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.domain.interfaces.branch_repo import BranchRepository
from src.presentation.api.v1.dependencies.dependencies import get_db_session
from src.core.application.use_cases.get_branch_use_case import GetBranchUseCase
from src.core.application.use_cases.get_branches_use_case import GetBranchesUseCase
from src.core.application.use_cases.delete_branches_use_case import DeleteBranchUseCase
from src.core.application.use_cases.post_branches_use_case import PostBranchesUseCase
from src.core.application.use_cases.put_branch_use_case import PutBranchUseCase

from src.infrastructure.database.dao.branch_dao import BranchDAO
from src.infrastructure.database.repositories.branch_repo_impl import BranchRepositoryImpl

def get_branch_repo(session: AsyncSession = Depends(get_db_session)) -> BranchRepository:
    return BranchRepositoryImpl(branch_dao = BranchDAO(session))

def get_branch_di(repo: BranchRepository = Depends(get_branch_repo)):
    return GetBranchUseCase(repo)

def get_branches_di(repo: BranchRepository = Depends(get_branch_repo)):
    return GetBranchesUseCase(repo)

def delete_branch_di(repo: BranchRepository = Depends(get_branch_repo)):
    return DeleteBranchUseCase(repo)

def post_branch_di(repo: BranchRepository = Depends(get_branch_repo)):
    return PostBranchesUseCase(repo)

def put_branch_di(repo: BranchRepository = Depends(get_branch_repo)):
    return PutBranchUseCase(repo)

