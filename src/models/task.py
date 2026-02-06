"""Task model and related schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Text
from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    """Base task model for shared fields."""

    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class Task(TaskBase, table=True):
    """Database task model."""

    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(nullable=False, index=True)
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(TaskBase):
    """Request model for creating tasks."""

    pass


class TaskUpdate(SQLModel):
    """Request model for updating tasks."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class TaskResponse(TaskBase):
    """Response model for task data."""

    id: UUID
    user_id: UUID
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
