from pydantic import BaseModel
        


class CategoryDTO(BaseModel):
    id: int
    name: str
    branch_id: int
    description: str
    is_active: bool
    

class CategoryCreateDTO(BaseModel):
    name: str
    branch_id: int
    description: str
    is_active: bool = True

class CategoriesDTO(BaseModel):    
    items: list[CategoryDTO]

class CategoryIdDTO(BaseModel):
    id: int

class CategoryUpdateDTO(BaseModel):
    name: str
    branch_id: int
    description: str
    is_active: bool = True

class GetCategoryInputDTO(BaseModel):
    branch_id: int
    limit: int
    offset: int