"""JWT token verification and security utilities."""

from datetime import datetime
from typing import Optional
from uuid import UUID

import jwt
from pydantic import BaseModel

from src.core.config import get_settings

settings = get_settings()

ALGORITHM = "HS256"


class TokenPayload(BaseModel):
    """JWT token payload structure."""

    sub: str  # user_id
    email: Optional[str] = None
    exp: Optional[datetime] = None
    iat: Optional[datetime] = None


class AuthenticatedUser(BaseModel):
    """Authenticated user information extracted from JWT."""

    id: UUID
    email: Optional[str] = None


def decode_token(token: str) -> Optional[TokenPayload]:
    """
    Decode and verify a JWT token.

    Args:
        token: The JWT token string

    Returns:
        TokenPayload if valid, None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=[ALGORITHM],
        )
        return TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_user_from_token(token: str) -> Optional[AuthenticatedUser]:
    """
    Extract user information from a JWT token.

    Args:
        token: The JWT token string

    Returns:
        AuthenticatedUser if valid, None if invalid
    """
    payload = decode_token(token)
    if payload is None:
        return None

    try:
        user_id = UUID(payload.sub)
        return AuthenticatedUser(id=user_id, email=payload.email)
    except (ValueError, TypeError):
        return None
