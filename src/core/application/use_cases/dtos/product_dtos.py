from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class ProductDTO(BaseModel):
    id: int | None
    name: str
    api_id: str | None
    uzname: str | None
    runame: str | None
    enname: str | None
    description: str
    image_url: str
    price: Decimal
    category_id: int
    subcategory_index: int
    branch_id: int
    is_active: bool
    maintenance_day: float | None
    maintenance_night: float | None

class ProductsDTO(BaseModel):
    products: list[ProductDTO]




class GetProductsInputDTO(BaseModel):
    branch_id: int = None
    category_id: int = None
    limit: int = 10
    offset: int = 0

class GetProductsDTO(BaseModel):
    category_id: Optional[int] = None
    limit: int = 10
    offset: int = 0
    current_user_id: Optional[int] = None
    current_user_role: Optional[str] = None



class GetProductInputDTO(BaseModel):
    product_id: int

class GetProductDTO(BaseModel):
    product_id: int
    current_user_id: Optional[int] = None
    current_user_role: Optional[str] = None


class ProductUpdateDTO(BaseModel):
    product_id: int
    name: str
    category_id: int
    branch_id: int
    description: str
    price: float
    is_active: bool
    maintenance_day: float | None
    maintenance_night: float | None
    current_user_id: Optional[int] = None
    current_user_role: Optional[str] = None

class ProductUpdateInputDTO(BaseModel):
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
    is_active: bool
    maintenance_day: float | None 
    maintenance_night: float | None
    current_user_id: Optional[int] = None
    current_user_role: Optional[str] = None

class ProductCreateInputDTO(BaseModel):
    name: str
    category_id: int
    branch_id: int
    description: str
    price: float
    is_active: bool
    maintenance_day: float | None 
    maintenance_night: float | None