from typing import Optional
from pydantic import BaseModel



class UserRegisterDTO(BaseModel):
    username: str
    password: str

class UserLogInDTO(BaseModel):
    username: str
    password: str


class UserCreateDTO(BaseModel):
    username: str
    password: str
    role: str

    
class UserResponseDTO(BaseModel):
    id: int
    username: str
    telegram_id: int
    role: str
    first_name: str
    branch_id: int


class UserLoginDTO(BaseModel):
    username: str
    password: str

    
class TokenDTO(BaseModel):
    access_token: str
    token_type: str


class TokenDataDTO(BaseModel):
    user_id: Optional[int] = None
    user_role: Optional[str] = None


class UserTelegramDTO(BaseModel):
    telegram_id: int
    username: str | None
    first_name: str

class UserTelegramInitionDTO(BaseModel):
    user: UserTelegramDTO
    username: str