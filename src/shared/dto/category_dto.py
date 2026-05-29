from pydantic import BaseModel
from typing import Optional
        


class CategoryDTO(BaseModel):
    name: str
    branch_id: int
    is_active: bool
    

class CategoryCreate(BaseModel):
    name: str
    branch_id: int
    is_active: bool = True