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

class PaymentLog(Base):
    __tablename__ = "payment_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    courier_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id"))
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    is_closed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    order: Mapped["Order"] = relationship(back_populates="payment_logs")
    courier: Mapped["User"] = relationship(back_populates="payment_logs")
    branch: Mapped["Branch"] = relationship(back_populates="payment_logs")

