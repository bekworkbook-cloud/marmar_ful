from datetime import datetime
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models import User
from src.infrastructure.database.models import Order


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Явно указываем foreign_keys, так как есть два пути к таблице User
    sender: Mapped["User"] = relationship(
        foreign_keys=[sender_id],
        back_populates="sends"
    )

    order: Mapped["Order"] = relationship(back_populates="messages")
