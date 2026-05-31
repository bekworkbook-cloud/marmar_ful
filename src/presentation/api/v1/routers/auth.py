from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.core.application.use_cases.register_user_use_case import RegisterUserUseCase
from src.core.application.use_cases.login_user_use_case import LogInUserUseCase
from src.core.application.use_cases.delete_user_self_use_case import DeleteUserSelfUseCase
from src.core.application.use_cases.verify_web_app_signature import VerifyWebAppSignatureUseCase
from src.core.application.use_cases.get_me_use_case import GetMeUseCase
from src.core.application.use_cases.dtos.auth_dtos import (
    UserRegisterDTO,
    TokenDTO,
    UserLogInDTO,
    TokenDataDTO,
    UserTelegramDTO,
    UserTelegramInitionDTO
)

from src.core.application.use_cases.dtos.user_dtos import UserDTO

from src.presentation.api.v1.dependencies.auth import (
    get_register_use_case,
    get_login_use_case,
    get_token_data,
    delete_user_self_use_case_di,
)
from src.presentation.api.v1.dependencies.user import (
    get_me_use_case_di,
)
from src.presentation.api.v1.dependencies.init_data import (
    verify_webapp_signature_dynamic,
    verify_webapp_signature_use_case
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=TokenDTO, include_in_schema=False)
async def swagger_token_proxy(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    use_case: LogInUserUseCase = Depends(get_login_use_case)
):
    user_dto = UserLogInDTO(
        username=form_data.username, 
        password=form_data.password
    )
    return await use_case.execute(user_login_dto=user_dto)


@router.post("/register", response_model=TokenDTO)
async def user_register(
    user_register: UserRegisterDTO, 
    use_case: RegisterUserUseCase = Depends(get_register_use_case)
):
    return await use_case.execute(user_register=user_register)


@router.post("/login", response_model=TokenDTO)
async def user_login(
    user_login_dto: UserLogInDTO,
    use_case: LogInUserUseCase = Depends(get_login_use_case)
):
    return await use_case.execute(user_login_dto=user_login_dto)


@router.delete("/delete", response_model=UserDTO)
async def user_delete(
    token_data: TokenDataDTO = Depends(get_token_data),
    use_case: DeleteUserSelfUseCase = Depends(delete_user_self_use_case_di)
):
    return await use_case.execute(token_data=token_data)


@router.get("/me", response_model=UserDTO)
async def get_me(
    token_dto: TokenDataDTO = Depends(get_token_data),
    use_case: GetMeUseCase = Depends(get_me_use_case_di)
):
    return await use_case.execute(token_dto=token_dto)


@router.post("/init_data/{bot}", response_model=TokenDTO)
async def tg_init_data(
    bot: str,
    init_data: dict = Depends(verify_webapp_signature_dynamic),
    use_case: VerifyWebAppSignatureUseCase = Depends(verify_webapp_signature_use_case)
):
    user_data = init_data.get("user", {})
    user=UserTelegramDTO(
            telegram_id=user_data.get("id"),
            username=user_data.get("username"),
            first_name=user_data.get("first_name")
        )
    user_telegram = UserTelegramInitionDTO(
        user=user,
        username=user_data.get("username")
    )
    token = await use_case.execute(user_telegram_inition_dto=user_telegram)
    print(f"token: {token}")
    return token
