from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger,
    Boolean,
    String,
    Text,
    DateTime,
    Float,
    Numeric,
    ForeignKey,
    UniqueConstraint,
    func
)

from src.infrastructure.database.models.base import Base


class Branch(Base):
    __tablename__ = "branches"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    branch_code: Mapped[Optional[str]] = mapped_column(String(20))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    address: Mapped[Optional[str]] = mapped_column(String(255))
    landmark: Mapped[Optional[str]] = mapped_column(String(255))
    latitude: Mapped[Optional[float]] = mapped_column(Float)
    longitude: Mapped[Optional[float]] = mapped_column(Float)
    delivery_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    personnel: Mapped[List["User"]] = relationship(back_populates="branch")
    categories: Mapped[List["Category"]] = relationship(back_populates="branch")
    products: Mapped[List["Product"]] = relationship(back_populates="branch")
    orders: Mapped[List["Order"]] = relationship(back_populates="branch")
    payment_logs: Mapped[List["PaymentLog"]] = relationship(back_populates="branch")
