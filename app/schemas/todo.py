from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class TodoBase(BaseModel):
    task: str = Field(..., min_length=1, description="Task description")
    completed: bool = Field(False, description="Task completion status")

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    task: Optional[str] = Field(None, min_length=1, description="Updated task description")
    completed: Optional[bool] = None

class TodoResponse(TodoBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TodoListResponse(BaseModel):
    todos: list[TodoResponse] = Field(..., description="List of todo items")
    total: int = Field(..., description="Total number of todo items")

    class Config:
        from_attributes = True  

class TodoDeleteResponse(BaseModel):
    message: str = Field(..., description="Confirmation message for deletion")

    class Config:
        from_attributes = True

class TodoCountResponse(BaseModel):
    count: int = Field(..., description="Total number of todo items")

    class Config:
        from_attributes = True
