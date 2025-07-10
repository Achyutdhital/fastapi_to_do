from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.user import User
from ..models.todo import Todo
from ..schemas.todo import (
    TodoCreate, 
    TodoUpdate, 
    TodoResponse, 
    TodoListResponse,
    TodoDeleteResponse
)
from ..core.security import get_current_user

# Create router instance
router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)

@router.get("/", response_model=TodoListResponse)
def get_todos(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get paginated list of user's todos.
    
    - **skip**: Number of todos to skip (for pagination)
    - **limit**: Maximum number of todos to return (1-100)
    - **completed**: Optional filter by completion status (true/false)
    
    Returns paginated list with total count.
    """
    
    # Build query for current user's todos
    query = db.query(Todo).filter(Todo.user_id == current_user.id)
    
    # Apply completed filter if provided
    if completed is not None:
        query = query.filter(Todo.completed == completed)
    
    # Get total count
    total = query.count()
    
    # Apply pagination and get todos
    todos = query.offset(skip).limit(limit).all()
    
    return TodoListResponse(
        todos=todos,
        total=total
    )

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo_data: TodoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new todo item.
    
    - **task**: Task description (required, minimum 1 character)
    - **completed**: Completion status (optional, defaults to false)
    """
    
    # Create new todo
    new_todo = Todo(
        task=todo_data.task,
        completed=todo_data.completed,
        user_id=current_user.id
    )
    
    # Save to database
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    return new_todo

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific todo by ID.
    
    Users can only access their own todos.
    """
    
    # Find todo
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    return todo

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing todo (partial updates allowed).
    
    - **task**: Updated task description (optional)
    - **completed**: Updated completion status (optional)
    
    Users can only update their own todos.
    """
    
    # Find todo
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    # Update fields that were provided
    update_data = todo_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(todo, field, value)
    
    # Save changes
    db.commit()
    db.refresh(todo)
    
    return todo

@router.patch("/{todo_id}", response_model=TodoResponse)
def patch_todo(
    todo_id: int,
    todo_patch: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Partially update a todo item (PATCH method).
    
    - **task**: Updated task description (optional)
    - **completed**: Updated completion status (optional)
    
    Only updates fields that are provided. Users can only update their own todos.
    """
    
    # Find todo
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    # Update only provided fields
    patch_data = todo_patch.dict(exclude_unset=True)
    
    if not patch_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )
    
    for field, value in patch_data.items():
        setattr(todo, field, value)
    
    # Save changes
    db.commit()
    db.refresh(todo)
    
    return todo


@router.delete("/{todo_id}", response_model=TodoDeleteResponse)
def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a specific todo.
    
    Users can only delete their own todos.
    """
    
    # Find todo
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    # Delete todo
    db.delete(todo)
    db.commit()
    
    return TodoDeleteResponse(
        message=f"Todo '{todo.task}' deleted successfully"
    )

@router.get("/stats/count", response_model=dict)
def get_todo_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get todo statistics for current user.
    
    Returns counts of total, completed, and pending todos.
    """
    
    # Get counts
    total = db.query(Todo).filter(Todo.user_id == current_user.id).count()
    completed = db.query(Todo).filter(
        Todo.user_id == current_user.id,
        Todo.completed == True
    ).count()
    pending = total - completed
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "completion_rate": round((completed / total * 100) if total > 0 else 0, 1)
    }