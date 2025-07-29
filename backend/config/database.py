from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database URL
DATABASE_URL = "sqlite:///./smart_locker.db"

# Create engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    face_image_path = Column(String, nullable=True)  # Path to registered face image
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Face data model
class FaceData(Base):
    __tablename__ = "face_data"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    face_encoding = Column(Text)  # Store face encoding as text
    image_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Locker model
class Locker(Base):
    __tablename__ = "lockers"
    
    id = Column(Integer, primary_key=True, index=True)
    locker_number = Column(String, unique=True, index=True)
    is_occupied = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=True)
    current_user_id = Column(Integer, nullable=True)
    last_accessed = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Access log model
class AccessLog(Base):
    __tablename__ = "access_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    locker_id = Column(Integer, index=True)
    action = Column(String)  # "open", "close", "lock", "unlock"
    success = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.utcnow)
    face_recognition_confidence = Column(Integer, nullable=True)  # 0-100 