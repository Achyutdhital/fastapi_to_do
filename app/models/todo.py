from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    task = Column(String, nullable=False)
    completed = Column(Boolean, server_default='FALSE', nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="todos")

    def __repr__(self):
        return f"<Todo(id={self.id}, task='{self.task}', completed={self.completed})>"