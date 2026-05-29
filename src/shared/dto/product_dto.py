from pydantic import BaseModel
        

class ProductDTO(BaseModel):
    id: int
    name: str
    category_id: int
    branch_id: int
    description: str
    price: float
    is_active: bool

class ProductCreateDTO(BaseModel):
    name: str
    category_id: int
    branch_id: int
    description: str
    price: float    
    is_active: bool = True