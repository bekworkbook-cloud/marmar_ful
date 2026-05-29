from pydantic import BaseModel
from typing import Optional
        

class MessageDTO(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    order_id: int
    text: str
    created_at: str


class MessageCreate(BaseModel):
    sender_id: int
    recipient_id: int
    order_id: int
    text: str

class MessagesDTO(BaseModel):
    messages: list[MessageDTO]  