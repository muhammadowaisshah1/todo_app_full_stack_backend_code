"""Authentication endpoints."""

from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

import jwt
from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel

from src.core.config import get_settings
from src.models.user import UserCreate, UserLogin, TokenResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory user storage (in production, use database)
# This is a simple implementation for the hackathon
users_db: dict[str, dict] = {}


def hash_password(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: str, email: str, name: str) -> str:
    """Create a JWT access token."""
    expire = datetime.utcnow() + timedelta(days=7)
    payload = {
        "sub": user_id,
        "email": email,
        "name": name,
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, settings.BETTER_AUTH_SECRET, algorithm="HS256")


@router.post("/signup", response_model=dict)
async def signup(user_data: UserCreate):
    """
    Register a new user.

    Returns success message with user_id.
    """
    # Check if email already exists
    email_lower = user_data.email.lower()
    if email_lower in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "DUPLICATE_EMAIL",
                "message": "Email already registered",
            },
        )

    # Create user
    user_id = str(uuid4())
    users_db[email_lower] = {
        "id": user_id,
        "email": email_lower,
        "name": user_data.name,
        "hashed_password": hash_password(user_data.password),
        "created_at": datetime.utcnow().isoformat(),
    }

    return {"message": "User created successfully", "user_id": user_id}


@router.post("/signin", response_model=TokenResponse)
async def signin(credentials: UserLogin):
    """
    Authenticate a user and return a JWT token.
    """
    email_lower = credentials.email.lower()

    # Find user
    user = users_db.get(email_lower)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "INVALID_CREDENTIALS",
                "message": "Invalid email or password",
            },
        )

    # Verify password
    if not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "INVALID_CREDENTIALS",
                "message": "Invalid email or password",
            },
        )

    # Create token
    access_token = create_access_token(user["id"], user["email"], user["name"])

    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
        ),
    )
