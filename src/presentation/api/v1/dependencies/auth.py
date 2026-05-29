from fastapi import Depends
from src.config import auth_pwd
from src.core.domain.services.auth_service import AuthService
from src.core.application.use_cases.login_user_use_case import LogInUserUseCase
from src.core.application.use_cases.register_user_use_case import RegisterUserUseCase
from src.core.application.use_cases.delete_user_self_use_case import DeleteUserSelfUseCase
from src.core.domain.interfaces.user_repo import UserRepository
from src.infrastructure.security.auth import verify_token
from src.presentation.api.v1.dependencies.user import get_user_repo
from src.presentation.api.v1.dependencies.services import get_auth_service




def check_token(token: str = Depends(auth_pwd.oauth2_schema)):
    verify_token(token)

def get_token_data(token: str = Depends(auth_pwd.oauth2_schema)):
    token_data = verify_token(token)

    return token_data

def get_current_active_user():
    pass

def get_register_use_case(
        repo: UserRepository = Depends(get_user_repo),
        auth_service: AuthService = Depends(get_auth_service)) -> RegisterUserUseCase:
    return RegisterUserUseCase(repo, auth_service)


def get_login_use_case(
        repo: UserRepository = Depends(get_user_repo),
        auth_service: AuthService = Depends(get_auth_service)
        ) -> LogInUserUseCase:
    return LogInUserUseCase(user_repo=repo, auth_service=auth_service)

def delete_user_self_use_case_di(repo: UserRepository = Depends(get_user_repo)) -> DeleteUserSelfUseCase:
    return DeleteUserSelfUseCase(repo)