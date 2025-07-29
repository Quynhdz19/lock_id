from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.routes.face_recognition_simple import router as face_router

app = FastAPI(
    title="Smart Locker API (Simple Demo)",
    description="Simple API for Smart Locker with Face Recognition Demo",
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

# Include routers
app.include_router(face_router, prefix="/api/face", tags=["Face Recognition"])

@app.get("/")
async def root():
    return {"message": "Smart Locker API (Simple Demo) is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Smart Locker API (Simple Demo)"}

if __name__ == "__main__":
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 