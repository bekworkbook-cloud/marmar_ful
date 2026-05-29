from decimal import Decimal
from pydantic import BaseModel, Field



class BranchDTO(BaseModel):
    id: int
    name: str
    branch_code: str
    description: str
    address: str
    landmark: str
    latitude: float
    longitude: float
    delivery_price: Decimal = Field(0.0, ge=0, example=299.99)
    is_active: bool


class BranchCreateDTO(BaseModel):
    name: str
    branch_code: str
    description: str
    address: str 
    landmark: str
    latitude: float
    longitude: float
    delivery_price: float = Field(0.0, ge=0, example=299.99)
    is_active: bool = True

class BranchesDTO(BaseModel):
    branches: list[BranchDTO]

class BranchIdDTO(BaseModel):
    id: int 


class BranchUpdateDTO(BaseModel):
    name: str
    branch_code: str
    description: str
    address: str 
    landmark: str
    latitude: float
    longitude: float
    delivery_price: float
    is_active: bool = True

class DeleteBranchDTO(BaseModel):
    id: int

