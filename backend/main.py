from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
import os
from dotenv import load_dotenv

from api.routes import auth, face_recognition, locker
from config.database import engine, Base

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Locker API",
    description="API for Smart Locker with Face Recognition",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Flutter app domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(face_recognition.router, prefix="/api/face", tags=["Face Recognition"])
app.include_router(locker.router, prefix="/api/locker", tags=["Locker Control"])

@app.get("/")
async def root():
    return {"message": "Smart Locker API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Smart Locker API"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 