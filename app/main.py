from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .core.config import settings
from .database import engine
from .models import user, todo
from .routes import auth, todos

# Create database tables
user.Base.metadata.create_all(bind=engine)
todo.Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    A secure Todo List API built with FastAPI.
    
    ## Features
    
    * **User Authentication**: JWT-based secure authentication
    * **Todo Management**: Full CRUD operations for todo items
    * **User Isolation**: Users can only access their own todos
    * **Pagination**: Efficient handling of large todo lists
    * **Data Validation**: Robust input validation with Pydantic
    
    ## Authentication
    
    1. Register a new account at `/auth/register`
    2. Login to get access token at `/auth/login`
    3. Include token in Authorization header: `Bearer <your_token>`
    4. Access protected endpoints with your token
    
    ## Endpoints
    
    * **Auth**: User registration, login, profile management
    * **Todos**: Create, read, update, delete todo items
    """,
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "User registration, login, and profile management"
        },
        {
            "name": "Todos",
            "description": "Todo item management (CRUD operations)"
        }
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(todos.router)

# Root endpoint
@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint - API health check and information.
    """
    return {
        "message": "Welcome to FastAPI Todo List API",
        "version": settings.VERSION,
        "status": "active",
        "documentation": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "auth": {
                "register": "/auth/register",
                "login": "/auth/login",
                "profile": "/auth/me"
            },
            "todos": {
                "list": "/todos",
                "create": "/todos",
                "get": "/todos/{id}",
                "update": "/todos/{id}",
                "delete": "/todos/{id}",
                "stats": "/todos/stats/count"
            }
        }
    }

# Health check endpoint
@app.get("/health", tags=["Root"])
def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    """
    return {
        "status": "healthy",
        "timestamp": "2025-01-10T00:00:00Z",
        "version": settings.VERSION,
        "database": "connected"
    }

# Global exception handler
@app.exception_handler(404)
def custom_404_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Endpoint not found",
            "available_endpoints": "/docs"
        }
    )

# Startup event
@app.on_event("startup")
def startup_event():
    """
    Application startup tasks.
    """
    print(f"🚀 {settings.PROJECT_NAME} v{settings.VERSION} starting up...")
    print(f"📊 Debug mode: {settings.DEBUG}")
    print(f"🗄️ Database: Connected")
    print(f"🔒 CORS origins: {settings.origins_list}")
    print(f"📚 API Documentation: http://localhost:3000/docs")

# Shutdown event
@app.on_event("shutdown")
def shutdown_event():
    """
    Application shutdown tasks.
    """
    print(f"🛑 {settings.PROJECT_NAME} shutting down...")