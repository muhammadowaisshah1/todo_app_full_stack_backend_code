"""Task business logic service."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task import Task, TaskCreate, TaskUpdate


async def get_tasks(
    session: AsyncSession,
    user_id: UUID,
    status_filter: Optional[str] = None,
) -> list[Task]:
    """
    Get all tasks for a user with optional status filter.

    Args:
        session: Database session
        user_id: User ID to filter by
        status_filter: Optional filter - "pending", "completed", or None for all

    Returns:
        List of tasks
    """
    query = select(Task).where(Task.user_id == user_id)

    if status_filter == "pending":
        query = query.where(Task.is_completed == False)
    elif status_filter == "completed":
        query = query.where(Task.is_completed == True)

    query = query.order_by(Task.created_at.desc())
    result = await session.execute(query)
    return list(result.scalars().all())


async def get_task(
    session: AsyncSession,
    task_id: UUID,
    user_id: UUID,
) -> Optional[Task]:
    """
    Get a single task by ID with ownership check.

    Args:
        session: Database session
        task_id: Task ID
        user_id: User ID for ownership verification

    Returns:
        Task if found and owned by user, None otherwise
    """
    query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def create_task(
    session: AsyncSession,
    user_id: UUID,
    task_data: TaskCreate,
) -> Task:
    """
    Create a new task.

    Args:
        session: Database session
        user_id: Owner user ID
        task_data: Task creation data

    Returns:
        Created task
    """
    task = Task(
        user_id=user_id,
        title=task_data.title.strip(),
        description=task_data.description.strip() if task_data.description else None,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def update_task(
    session: AsyncSession,
    task: Task,
    task_data: TaskUpdate,
) -> Task:
    """
    Update an existing task.

    Args:
        session: Database session
        task: Task to update
        task_data: Update data

    Returns:
        Updated task
    """
    if task_data.title is not None:
        task.title = task_data.title.strip()
    if task_data.description is not None:
        task.description = task_data.description.strip() or None

    task.updated_at = datetime.utcnow()
    await session.commit()
    await session.refresh(task)
    return task


async def toggle_task_completion(
    session: AsyncSession,
    task: Task,
) -> Task:
    """
    Toggle task completion status.

    Args:
        session: Database session
        task: Task to toggle

    Returns:
        Updated task
    """
    task.is_completed = not task.is_completed
    task.updated_at = datetime.utcnow()
    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(
    session: AsyncSession,
    task: Task,
) -> None:
    """
    Delete a task.

    Args:
        session: Database session
        task: Task to delete
    """
    await session.delete(task)
    await session.commit()
