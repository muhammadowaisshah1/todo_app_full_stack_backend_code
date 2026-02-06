# Backend Guidelines - Todo App (FastAPI)

## Technology Stack
- **Framework**: FastAPI 0.115+
- **Language**: Python 3.11+
- **ORM**: SQLModel (async)
- **Database**: Neon Serverless PostgreSQL
- **Validation**: Pydantic 2.x
- **Auth**: JWT verification via PyJWT

## Project Structure
```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py             # Dependency injection (get_current_user)
│   │   ├── health.py           # Health check endpoint
│   │   ├── tasks.py            # Task CRUD endpoints
│   │   └── responses.py        # Standardized response models
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py             # Task SQLModel
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py     # Task business logic
│   └── core/
│       ├── __init__.py
│       ├── config.py           # Settings with pydantic-settings
│       ├── database.py         # Async SQLModel engine
│       ├── security.py         # JWT decode/verify
│       └── middleware.py       # Auth middleware
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # pytest fixtures
│   ├── test_health.py
│   └── test_tasks.py
├── .env.example
├── requirements.txt
├── pyproject.toml
└── CLAUDE.md
```

## API Patterns

### Endpoint Structure
```python
@router.get("/{user_id}/tasks", response_model=APIResponse[list[TaskResponse]])
async def get_tasks(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    status: Optional[str] = None
) -> APIResponse[list[TaskResponse]]:
    verify_user_access(user_id, current_user)
    tasks = await task_service.get_tasks(session, user_id, status)
    return APIResponse(success=True, data=tasks)
```

### Response Format
```python
class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[ErrorDetail] = None

class ErrorDetail(BaseModel):
    code: str
    message: str
```

## Authentication

### JWT Verification
```python
# core/security.py
def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.BETTER_AUTH_SECRET,
        algorithms=["HS256"]
    )
```

### User Access Verification
```python
# api/deps.py
def verify_user_access(url_user_id: UUID, current_user: User):
    if str(url_user_id) != str(current_user.id):
        raise HTTPException(status_code=404, detail="Task not found")
```

## Database Patterns

### Async Queries
```python
async def get_tasks(session: AsyncSession, user_id: UUID) -> list[Task]:
    query = select(Task).where(Task.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().all()
```

### Always Filter by user_id
Every task query MUST include `Task.user_id == authenticated_user_id`

## Error Handling

### Error Codes
- `VALIDATION_ERROR`: Invalid input (400)
- `AUTHENTICATION_REQUIRED`: No/invalid token (401)
- `FORBIDDEN`: Authenticated but not authorized (403)
- `NOT_FOUND`: Resource doesn't exist (404)
- `INTERNAL_ERROR`: Server error (500)

### HTTPException Pattern
```python
if not task:
    raise HTTPException(
        status_code=404,
        detail={"code": "NOT_FOUND", "message": "Task not found"}
    )
```

## Security Requirements
1. JWT verification on ALL protected endpoints
2. user_id in URL MUST match JWT user_id
3. All queries filter by authenticated user_id
4. No secrets in code (use environment variables)
5. CORS restricted to frontend origin

## Running the Application

### Development
```bash
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```

### Testing
```bash
pytest
ruff check .
black --check .
```

## Code Quality
- Run `black .` before commits
- Run `ruff check .` for linting
- Type hints on all function signatures
- Docstrings on public functions
