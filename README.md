# FastAPI Todo Application

A secure, scalable Todo List API built with FastAPI, featuring JWT authentication and PostgreSQL database support.

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
3. Set up PostgreSQL database
4. Configure environment variables in `.env`
5. Run: `uvicorn app.main:app --reload`
6. Visit: http://localhost:8000/docs

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /auth/me` - Get user profile
- `PUT /auth/me` - Update profile
- `PUT /auth/me/password` - Change password (requires current password)

### Todos
- `GET /todos` - Get user's todos (paginated)
- `POST /todos` - Create new todo
- `GET /todos/{id}` - Get specific todo
- `PUT /todos/{id}` - Update todo
- `PATCH /todos/{id}` - Partial update
- `DELETE /todos/{id}` - Delete todo
- `GET /todos/stats/count` - Get statistics

## Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration (PostgreSQL)
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/fastapi_todo

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
DEBUG=True
ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

**Important:** Replace `your_password` with your actual PostgreSQL password.

### Alternative: SQLite (for testing)
If you prefer SQLite for easy setup:
```env
DATABASE_URL=sqlite:///./fastapi_todo.db
```

## Technology Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Primary database (SQLite also supported)
- **Pydantic** - Data validation using Python type hints
- **JWT** - JSON Web Tokens for authentication
- **Bcrypt** - Password hashing
- **psycopg2** - PostgreSQL adapter for Python

## Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 12+ (with psycopg2 driver included in requirements.txt)

### Database Setup (PostgreSQL)

1. **Install PostgreSQL**
   - Download from: https://www.postgresql.org/download/
   - Install and remember the password for `postgres` user

2. **Create Database**
   ```bash
   # Connect to PostgreSQL
   psql -U postgres
   
   # Create database
   CREATE DATABASE fastapi_todo;
   
   # Exit
   \q
   ```

3. **Update .env file**
   ```env
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/fastapi_todo
   ```

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd todo_fastapi
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create `.env` file in project root (see Environment Variables section above)

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the API**
   - **Interactive Docs**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc
   - **API Root**: http://localhost:8000/

## 🔁 Postman API Testing

A complete Postman collection is available for testing all API endpoints.

### 🧪 How to Use

1. Import `fastapi-todo.postman_collection.json` into Postman
2. Select or create environment:
   - `base_url = http://127.0.0.1:8000`
3. Run the following requests in order:

   1. Register User
   2. Login User (automatically sets `{{token}}`)
   3. Get Profile
   4. Create Todo (automatically sets `{{todo_id}}`)
   5. Get Todo by ID
   6. Update or Patch Todo
   7. Delete Todo
   8. Get Stats
   9. Refresh Token
   10. Health Check

### ✅ Environment Variables Used

| Variable     | Example Value              | Notes                        |
|--------------|----------------------------|------------------------------|
| `base_url`   | `http://127.0.0.1:8000`     | Your local FastAPI server    |
| `token`      | `Bearer <access_token>`    | Set automatically on login   |
| `todo_id`    | `Integer`                  | Set automatically on create  |
| `refresh_token` | `string`                | Optional, for token refresh  |

### First Time Setup (Per Device)
1. Import the Postman collection
2. Create environment with `base_url = http://127.0.0.1:8000`
3. Login once to auto-populate the token
4. All endpoints will work automatically

## Password Change Security

The password change endpoint requires both current and new passwords for security:

```json
PUT /auth/me/password
{
    "current_password": "your_current_password",
    "new_password": "your_new_password"
}
```

**Security Features:**
- Current password verification required
- New password must meet complexity requirements (8+ chars, uppercase, number)
- JWT authentication required
- Invalid current password returns 400 error

## Testing Results

### ✅ Authentication Tests
- [x] User registration with validation
- [x] User login with JWT token generation
- [x] Password change with current password verification
- [x] Profile updates (name, email)
- [x] Token refresh functionality

### ✅ Todo Management Tests
- [x] Create todo items
- [x] Retrieve paginated todos
- [x] Filter todos by completion status
- [x] Update todos (full and partial)
- [x] Delete todos
- [x] Todo statistics

### ✅ Security Tests
- [x] User isolation (users only see their own todos)
- [x] JWT token validation
- [x] Password complexity requirements
- [x] Email uniqueness validation
- [x] Proper error handling (401, 400, 404)

### ✅ API Features
- [x] Interactive documentation at `/docs`
- [x] Pagination with skip/limit
- [x] Input validation with clear error messages
- [x] Auto-generated timestamps
- [x] CORS configuration for frontend integration

## Project Structure

```
todo_fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app configuration
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # App configuration
│   │   └── security.py         # JWT & password handling
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # User database model
│   │   └── todo.py             # Todo database model
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py             # Authentication routes
│   │   └── todos.py            # Todo CRUD routes
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # User Pydantic schemas
│   │   └── todo.py             # Todo Pydantic schemas
│   └── database.py             # Database configuration
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── fastapi-todo.postman_collection.json  # API testing collection
└── (PostgreSQL database - external)
```

## Troubleshooting

### Database Connection Issues
- **Error**: `connection to server failed`
  - Solution: Ensure PostgreSQL is running
  - Check: `pg_ctl status` or Services (Windows)

- **Error**: `database "fastapi_todo" does not exist`
  - Solution: Create database using `CREATE DATABASE fastapi_todo;`

- **Error**: `authentication failed`
  - Solution: Verify username/password in DATABASE_URL

### Common Issues
- **Port already in use**: Change port with `--port 8001`
- **Module not found**: Activate virtual environment
- **Permission denied**: Run as administrator (Windows)

## Development

### Adding New Features
1. Create new routes in `app/routes/`
2. Add corresponding schemas in `app/schemas/`
3. Update models if needed in `app/models/`
4. Test with Postman collection

### Database Changes
- Models use SQLAlchemy ORM
- Database tables auto-created on startup
- Timestamps (created_at, updated_at) auto-managed

## Security Features

- 🔐 **JWT Authentication** - Stateless, secure tokens
- 🔒 **Password Hashing** - Bcrypt with salt
- 🛡️ **Input Validation** - Pydantic schema validation
- 🚫 **User Isolation** - Users only access their own data
- ✅ **CORS Configuration** - Secure cross-origin requests
- 🔑 **Token Expiration** - Automatic token lifecycle

## API Documentation

Visit `/docs` for interactive API documentation with:
- Complete endpoint reference
- Request/response examples
- Authentication testing
- Schema validation details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please open an issue on GitHub.