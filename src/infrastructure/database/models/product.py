import enum
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

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    api_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    uzname: Mapped[Optional[str]] = mapped_column(String(255))
    runame: Mapped[Optional[str]] = mapped_column(String(255))
    enname: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    img: Mapped[str] = mapped_column(String(255))
    image_url: Mapped[Optional[str]] = mapped_column(String(255))
    img_file_id: Mapped[Optional[str]] = mapped_column(String(255))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    subcategoryindex: Mapped[int] = mapped_column()
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    maintenance_day: Mapped[Optional[str]] = mapped_column(String(255))
    maintenance_night: Mapped[Optional[str]] = mapped_column(String(255))

    category: Mapped["Category"] = relationship(back_populates="products")
    branch: Mapped["Branch"] = relationship(back_populates="products")
    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="product")
