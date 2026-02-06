# Todo App Backend - FastAPI

A production-ready FastAPI backend for a multi-user todo application with JWT authentication.

## 🚀 Features

- ✅ RESTful API with FastAPI
- 🔐 JWT Authentication
- 🗄️ PostgreSQL with SQLModel ORM
- 🔒 User isolation and security
- 📝 Async/await throughout
- ✨ Type-safe with Pydantic
- 🧪 Comprehensive test coverage

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL database (Neon recommended)
- pip or poetry

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone <your-backend-repo-url>
cd backend
```

### 2. Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/database

# Authentication (MUST match frontend)
BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters

# Application
APP_NAME=Todo API
APP_VERSION=1.0.0
ENVIRONMENT=production

# Frontend URL (for CORS)
FRONTEND_URL=https://your-frontend-domain.com
```

**⚠️ CRITICAL**: `BETTER_AUTH_SECRET` must be identical in both frontend and backend!

## 🏃 Running the Application

### Development

```bash
uvicorn src.main:app --reload --port 8000
```

### Production

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_tasks.py
```

## 📚 API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/signin` - Login user

### Tasks (Protected)
- `GET /api/{user_id}/tasks` - Get all tasks
- `POST /api/{user_id}/tasks` - Create task
- `GET /api/{user_id}/tasks/{id}` - Get task by ID
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

### Health
- `GET /api/health` - Health check

## 🚢 Deployment

### Railway

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login and deploy:
```bash
railway login
railway init
railway up
```

3. Add environment variables in Railway dashboard

### Render

1. Create new Web Service
2. Connect your GitHub repository
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables

### Docker

```bash
# Build image
docker build -t todo-backend .

# Run container
docker run -p 8000:8000 --env-file .env todo-backend
```

## 🔒 Security Features

- JWT token verification on all protected routes
- User isolation (users can only access their own data)
- SQL injection prevention via SQLModel
- CORS restricted to frontend origin
- Environment-based secrets
- Password hashing with bcrypt

## 📁 Project Structure

```
backend/
├── src/
│   ├── api/              # API endpoints
│   ├── core/             # Core functionality (config, db, auth)
│   ├── models/           # Database models
│   ├── services/         # Business logic
│   └── main.py           # Application entry point
├── tests/                # Test suite
├── .env.example          # Environment template
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker configuration
└── README.md            # This file
```

## 🐛 Troubleshooting

### Database Connection Issues
- Verify `DATABASE_URL` format: `postgresql+asyncpg://user:pass@host:port/db`
- Check database is accessible from your network
- For Neon, ensure you're using the pooled connection string

### JWT Authentication Fails
- Ensure `BETTER_AUTH_SECRET` matches frontend exactly
- Check token is sent in `Authorization: Bearer <token>` header
- Verify token hasn't expired

### CORS Errors
- Update `FRONTEND_URL` in `.env` to match your frontend domain
- Include protocol (https://) in URL

## 📝 Code Quality

```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy src/
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review API docs at `/docs`

---

Built with ❤️ using FastAPI
