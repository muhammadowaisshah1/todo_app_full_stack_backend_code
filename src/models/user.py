"""User model for authentication."""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Request model for user registration."""

    email: EmailStr
    password: str = Field(min_length=8)
    name: str = Field(min_length=1, max_length=100)


class UserLogin(BaseModel):
    """Request model for user login."""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Response model for user data."""

    id: UUID
    email: str
    name: str


class TokenResponse(BaseModel):
    """Response model for authentication token."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse
