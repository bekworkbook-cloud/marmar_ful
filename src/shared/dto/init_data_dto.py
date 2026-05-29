from pydantic import BaseModel
from typing import Optional

class InitDataDTO(BaseModel):
    bot_name: str