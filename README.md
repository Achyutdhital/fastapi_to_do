# FastAPI Todo Application

A secure, scalable Todo List API built with FastAPI, featuring JWT authentication and PostgreSQL/SQLite database support.

## Features

- 🔐 **JWT Authentication** - Secure user authentication
- 👤 **User Management** - Registration, login, profile updates
- 📝 **Todo Management** - Full CRUD operations
- 🔒 **User Isolation** - Users only access their own data
- 📊 **Pagination & Filtering** - Efficient data handling
- 🛡️ **Input Validation** - Robust data validation
- 📚 **Auto Documentation** - Interactive API docs

## Quick Start

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.env`
4. Run: `uvicorn app.main:app --reload`
5. Visit: http://localhost:8000/docs

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /auth/me` - Get user profile
- `PUT /auth/me` - Update profile
- `PUT /auth/me/password` - Change password

### Todos
- `GET /todos` - Get user's todos (paginated)
- `POST /todos` - Create new todo
- `GET /todos/{id}` - Get specific todo
- `PUT /todos/{id}` - Update todo
- `PATCH /todos/{id}` - Partial update
- `DELETE /todos/{id}` - Delete todo
- `GET /todos/stats/count` - Get statistics

## Environment Variables

```
DATABASE_URL=sqlite:///./fastapi_todo.db
JWT_SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000
```

## Technology Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type hints
- **JWT** - JSON Web Tokens for authentication
- **Bcrypt** - Password hashing
- **PostgreSQL/SQLite** - Database options