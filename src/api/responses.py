"""Standardized API response models."""

from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ErrorDetail(BaseModel):
    """Error detail structure."""

    code: str
    message: str


class APIResponse(BaseModel, Generic[T]):
    """Standardized API response wrapper."""

    success: bool
    data: Optional[T] = None
    error: Optional[ErrorDetail] = None

    @classmethod
    def ok(cls, data: T) -> "APIResponse[T]":
        """Create a successful response."""
        return cls(success=True, data=data, error=None)

    @classmethod
    def fail(cls, code: str, message: str) -> "APIResponse[None]":
        """Create an error response."""
        return cls(success=False, data=None, error=ErrorDetail(code=code, message=message))


class MessageResponse(BaseModel):
    """Simple message response."""

    message: str
