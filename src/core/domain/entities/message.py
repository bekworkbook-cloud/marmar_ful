from datetime import datetime
from src.core.domain.exceptions.validation import DomainValidationError

class Message:
    def __init__(
        self,
        id: int | None,
        sender_id: int,
        order_id: int,
        text: str,
        created_at: datetime | None = None
    ):
        if not text.strip():
            raise DomainValidationError("Message text cannot be empty")
        
        self.id = id 
        self.sender_id = sender_id
        self.order_id = order_id
        self.text = text
        self.created_at = created_at or datetime.now()
