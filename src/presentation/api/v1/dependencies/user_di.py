from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.domain.interfaces.user_repo import UserRepository
from src.infrastructure.database.repositories.user_repo_impl import UserRepositoryImpl
from src.infrastructure.database.dao.user_dao import UserDAO
from src.presentation.api.v1.dependencies.dependencies import get_db_session
from src.presentation.api.v1.dependencies.services import get_auth_service

from src.core.domain.services.auth_service import AuthService

from src.core.application.use_cases.get_users_use_case import GetUsersUseCase
from src.core.application.use_cases.get_user_use_case import GetUserUseCase
from src.core.application.use_cases.post_user_use_case import PostUserUseCase
from src.core.application.use_cases.patch_user_use_case import PatchUserUseCase
from src.core.application.use_cases.delete_user_use_case import DeleteUserUseCase
from src.core.application.use_cases.put_user_use_case import PutUserUseCase

def get_user_repo(session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepositoryImpl(user_dao = UserDAO(session))

def get_users_use_case_di(repo: UserRepository = Depends(get_user_repo)):
    return GetUsersUseCase(repo)

def post_user_use_case_di(
        user_repo: UserRepository = Depends(get_user_repo),
        auth_service: AuthService = Depends(get_auth_service)):
    return PostUserUseCase(
        user_repo=user_repo,
        auth_service=auth_service
    )

def get_user_use_case_di(repo: UserRepository = Depends(get_user_repo)):
    return GetUserUseCase(repo)

def put_user_use_case_di(repo: UserRepository = Depends(get_user_repo)):
    return PutUserUseCase(repo)

def patch_user_use_case_di(repo: UserRepository = Depends(get_user_repo)):
    return PatchUserUseCase(repo)

def delete_user_use_case_di(repo: UserRepository = Depends(get_user_repo)):
    return DeleteUserUseCase(repo)