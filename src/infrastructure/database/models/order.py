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

from src.core.domain.enums.order_status import OrderStatus

from src.infrastructure.database.models.base import Base

class Order(Base):
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    operator_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    courier_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    branch_id: Mapped[Optional[int]] = mapped_column(ForeignKey("branches.id"))
    
    status: Mapped[str] = mapped_column(String(20), default=OrderStatus.PENDING.value)
    pay_method: Mapped[str] = mapped_column(String(20))
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    is_accepted: Mapped[bool] = mapped_column(Boolean, default=False)
    
    address: Mapped[Optional[str]] = mapped_column(Text)
    landmark: Mapped[Optional[str]] = mapped_column(String(255))
    latitude: Mapped[Optional[float]] = mapped_column(Float)
    longitude: Mapped[Optional[float]] = mapped_column(Float)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    customer: Mapped["User"] = relationship(
        foreign_keys=[customer_id], back_populates="orders_as_customer"
    )
    operator: Mapped[Optional["User"]] = relationship(
        foreign_keys=[operator_id], back_populates="orders_as_operator"
    )
    courier: Mapped[Optional["User"]] = relationship(
        foreign_keys=[courier_id], back_populates="orders_as_courier"
    )
    items: Mapped[List["OrderItem"]] = relationship(back_populates="order")
    branch: Mapped[Optional["Branch"]] = relationship(back_populates="orders")
    payment_logs: Mapped[List["PaymentLog"]] = relationship(back_populates="order")

