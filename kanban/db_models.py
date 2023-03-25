from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base
from kanban.enums import Colors


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[str] = mapped_column(nullable=False)
    is_important: Mapped[bool] = mapped_column(default=False)
    description: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    deadline: Mapped[datetime] = mapped_column(nullable=True)
    is_delete: Mapped[bool] = mapped_column(default=False)
    column_id: Mapped[int] = mapped_column(ForeignKey("columns.id"))
    column: Mapped["Column"] = relationship(back_populates="tasks")

    def __repr__(self) -> str:
        return f"Task id: {self.id}, title: {self.title}, code: {self.code}, is_important: {self.is_important}, " \
               f"description: {self.description}, created_at: {self.created_at}, updated_at: {self.updated_at}, " \
               f"deadline: {self.deadline}, is_delete: {self.is_delete}, column_id: {self.column_id}"


class Column(Base):
    __tablename__ = "columns"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    color: Mapped[str] = mapped_column(default=Colors.WHITE.value)
    sort: Mapped[int] = mapped_column(default=100)
    is_delete: Mapped[bool] = mapped_column(default=False)
    tasks: Mapped[Task | None] = relationship(back_populates="column")

    def __repr__(self) -> str:
        return f"Column id: {self.id}, code: {self.code}, title: {self.title}, color: {self.color}, " \
               f"sort: {self.sort}, is_delete: {self.is_delete}"


class Entities(Enum):
    COLUMN = Column
    TASK = Task
