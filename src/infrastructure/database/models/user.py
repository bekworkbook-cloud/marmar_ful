import enum
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger,
    String,
    DateTime,
    ForeignKey,
    func
)

from src.infrastructure.database.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=True)
    phone_number: Mapped[str] = mapped_column(String(255), nullable=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    hashed_pwd: Mapped[Optional[str]] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20))
    branch_id: Mapped[Optional[int]] = mapped_column(ForeignKey("branches.id"))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    branch: Mapped[Optional["Branch"]] = relationship(back_populates="personnel")
    orders_as_customer: Mapped[List["Order"]] = relationship(
        back_populates="customer",
        foreign_keys="[Order.customer_id]"
    )
    orders_as_operator: Mapped[List["Order"]] = relationship(
        back_populates="operator",
        foreign_keys="[Order.operator_id]"
    )
    orders_as_courier: Mapped[List["Order"]] = relationship(
        back_populates="courier",
        foreign_keys="[Order.courier_id]"
    )
    payment_logs: Mapped[List["PaymentLog"]] = relationship(back_populates="courier")

    sends: Mapped[List["Message"]] = relationship(
        back_populates="sender", 
        foreign_keys="[Message.sender_id]"
    )
