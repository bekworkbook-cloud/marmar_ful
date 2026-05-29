from pydantic import BaseModel


class UserDTO(BaseModel):
    id: str
    telegram_id: str
    first_name: str
    username: str
    hashed_pwd: str
    role: str
    branch_id: str

class UserCreateDTO(BaseModel):
    username: str
    password: str
    role: str
    branch_id: str

class UserIdDTO(BaseModel):
    id: str
