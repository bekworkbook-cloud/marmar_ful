from fastapi import Depends
from src.config import auth_pwd
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.domain.interfaces.user_repo import UserRepository
from src.infrastructure.database.repositories.user_repo_impl import UserRepositoryImpl
from src.infrastructure.database.dao.user_dao import UserDAO
from src.core.application.use_cases.get_me_use_case import GetMeUseCase
from src.core.application.use_cases.delete_user_use_case import DeleteUserUseCase 

from src.presentation.api.v1.dependencies.dependencies import get_db_session
from src.infrastructure.security.auth import verify_token


def get_user_repo(session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepositoryImpl(user_dao=UserDAO(session))

def get_current_user(token: str = Depends(auth_pwd.oauth2_schema), session: AsyncSession = Depends(get_db_session)):
    token_data = verify_token(token)
    user_repo = UserRepositoryImpl(UserDAO(session))

def get_me_use_case_di(repo: UserRepository = Depends(get_user_repo)) -> GetMeUseCase:
    return GetMeUseCase(repo)

def delete_user_use_case_di(repo: UserRepository = Depends(get_user_repo)) -> DeleteUserUseCase:
    return DeleteUserUseCase(repo)

