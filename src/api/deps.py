"""API dependencies for dependency injection."""

from uuid import UUID

from fastapi import HTTPException, status

from src.core.security import AuthenticatedUser


def verify_user_access(url_user_id: UUID, current_user: AuthenticatedUser) -> None:
    """
    Verify that the authenticated user has access to the requested resource.

    Args:
        url_user_id: The user_id from the URL path
        current_user: The authenticated user from JWT

    Raises:
        HTTPException: 404 if user doesn't have access (returns 404 to prevent enumeration)
    """
    if url_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NOT_FOUND",
                "message": "Resource not found",
            },
        )
