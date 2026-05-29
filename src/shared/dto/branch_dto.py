from pydantic import BaseModel
from decimal import Decimal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional


class BranchDTO(BaseModel):
    id: int
    name: str
    branch_code: str
    description: str
    address: str
    landmark: str
    latitude: float
    longitude: float
    delivery_price: Decimal
    is_active: bool


class BranchCreate(BaseModel):
    # id: Optional[int] = Field(None, description="Уникальный ID")
    name: str = Field(..., min_length=1, max_length=200, example="Филиал №1")
    branch_code: str = Field(..., min_length=3, max_length=20, example="B001")
    description: Optional[str] = Field(None, max_length=500)
    address: str = Field(..., min_length=5, example="ул. Ленина, 10")
    landmark: Optional[str] = Field(None, example="Рядом с метро")
    latitude: float = Field(..., ge=-90, le=90, example=55.7558)
    longitude: float = Field(..., ge=-180, le=180, example=37.6176)
    delivery_price: float = Field(0.0, ge=0, example=299.99)
    is_active: bool = Field(True)
