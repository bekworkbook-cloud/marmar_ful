from pydantic import BaseModel
from typing import Optional
from datetime import datetime
        

class MessageDTO(BaseModel):
    id: int
    sender_id: int
    order_id: int
    text: str
    created_at: str


class MessagePostDTO(BaseModel):
    order_id: Optional[int] = None
    text: str

class MessageCreateDTO(BaseModel):
    text: str
    order_id: int
    current_user_id: int
    current_user_role: str

class MessagesDTO(BaseModel):
    messages: list[MessageDTO]  

class GetMessagesInputDTO(BaseModel):
    order_id: int
    limit: int
    offset: int
    current_user_id: int
    current_user_role: str
