from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql.expression import text
from ..database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    todos = relationship("Todo", back_populates="user", cascade="all, delete-orphan")
