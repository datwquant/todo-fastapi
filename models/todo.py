from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from db.base import Base


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)

    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    is_done: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
   )

    due_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )
    
    # 🔥 THÊM 2 DÒNG QUAN TRỌNG NÀY
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner = relationship("User")