"""Task CRUD endpoints."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import verify_user_access
from src.core.database import get_session
from src.core.middleware import get_current_user
from src.core.security import AuthenticatedUser
from src.models.task import TaskCreate, TaskResponse, TaskUpdate
from src.services import task_service

router = APIRouter(tags=["tasks"])


@router.get("/{user_id}/tasks", response_model=list[TaskResponse])
async def get_tasks(
    user_id: UUID,
    current_user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    status: Optional[str] = Query(None, regex="^(pending|completed)$"),
):
    """
    Get all tasks for a user.

    Optional filter by status: pending, completed.
    """
    verify_user_access(user_id, current_user)
    tasks = await task_service.get_tasks(session, user_id, status)
    return tasks


@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: UUID,
    task_data: TaskCreate,
    current_user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Create a new task.
    """
    verify_user_access(user_id, current_user)
    task = await task_service.create_task(session, user_id, task_data)
    return task


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: UUID,
    task_id: UUID,
    current_user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get a single task by ID.
    """
    verify_user_access(user_id, current_user)
    task = await task_service.get_task(session, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Task not found"},
        )
    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: UUID,
    task_id: UUID,
    task_data: TaskUpdate,
    current_user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Update a task.
    """
    verify_user_access(user_id, current_user)
    task = await task_service.get_task(session, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Task not found"},
        )
    updated_task = await task_service.update_task(session, task, task_data)
    return updated_task


@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: UUID,
    task_id: UUID,
    current_user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Delete a task.
    """
    verify_user_access(user_id, current_user)
    task = await task_service.get_task(session, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Task not found"},
        )
    await task_service.delete_task(session, task)
    return None


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    user_id: UUID,
    task_id: UUID,
    current_user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Toggle task completion status.
    """
    verify_user_access(user_id, current_user)
    task = await task_service.get_task(session, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Task not found"},
        )
    updated_task = await task_service.toggle_task_completion(session, task)
    return updated_task
