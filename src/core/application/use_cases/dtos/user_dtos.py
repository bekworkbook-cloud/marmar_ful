from pydantic import BaseModel
from typing import Optional


class UserDTO(BaseModel):
    id: int
    telegram_id: Optional[int] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    phone_number: Optional[str] = None
    role: str
    branch_id: Optional[int] = None

    class Config:
        from_attributes = True

class UserCreateDTO(BaseModel):
    username: str
    password: str
    role: str
    branch_id: int

class UserIdDTO(BaseModel):
    id: str


class GetUserDTO(BaseModel):
    id: int
    telegram_id: int
    first_name: Optional[str] = None
    username: str
    role: str    
    branch_id: int

class GetUsersDTO(BaseModel):
    items: list[GetUserDTO]

class GetUsersInputDTO(BaseModel):
    role: str
    branch_id: Optional[int] = None
    limit: int
    offset: int

class GetUserInputDTO(BaseModel):
    user_id: int


class UserUpdateDTO(BaseModel):
    telegram_id: Optional[int] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    phone_number: Optional[str] = None
    role: str
    branch_id: Optional[int] = None


class DeleteUserDTO(BaseModel):
    user_id: int