from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
import uuid
from datetime import datetime

router = APIRouter()

# Simple in-memory storage for demo
REGISTERED_FACES = {}  # {user_id: "registered"}

# Directory to store face images
FACE_IMAGES_DIR = "face_recognition/data/faces"
os.makedirs(FACE_IMAGES_DIR, exist_ok=True)

def save_face_image(image_data: bytes, user_id: str) -> str:
    """Save face image to disk and return filename"""
    filename = f"user_{user_id}_{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(FACE_IMAGES_DIR, filename)
    
    with open(filepath, "wb") as f:
        f.write(image_data)
    
    return filename

# ============================================================================
# 1. FACE REGISTRATION API (Simple version)
# ============================================================================

@router.post("/register")
async def register_face(
    file: UploadFile = File(...),
    user_id: str = Form("owner"),  # Default to "owner" for demo
):
    """
    Register user's face for authentication (Simple version)
    """
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image data
        image_data = await file.read()
        
        # Save face image
        filename = save_face_image(image_data, user_id)
        
        # Store in memory (simple demo)
        REGISTERED_FACES[user_id] = "registered"
        
        print(f"✅ Face registered successfully for user: {user_id}")
        
        return {
            "success": True,
            "message": "Face registered successfully! You can now use face recognition to unlock your locker.",
            "user_id": user_id,
            "face_image_path": filename
        }
        
    except Exception as e:
        print(f"❌ Error registering face: {e}")
        raise HTTPException(status_code=500, detail=f"Error registering face: {str(e)}")

# ============================================================================
# 2. FACE VERIFICATION API (Simple version)
# ============================================================================

@router.post("/verify")
async def verify_face(
    file: UploadFile = File(...),
    user_id: str = Form("owner"),  # Default to "owner" for demo
):
    """
    Verify user's face for authentication (Simple version)
    """
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image data
        image_data = await file.read()
        
        # Check if user has registered face
        if user_id not in REGISTERED_FACES:
            raise HTTPException(status_code=400, detail="No face registered for this user. Please register your face first.")
        
        # Simple verification (always return success for demo)
        # In real implementation, you would compare face encodings here
        is_match = True  # Demo: always match
        
        if is_match:
            print(f"✅ Face verification successful for user: {user_id}")
            return {
                "success": True,
                "message": "Face verification successful! Identity confirmed.",
                "user_id": user_id,
                "confidence": 0.95
            }
        else:
            print(f"❌ Face verification failed for user: {user_id}")
            return {
                "success": False,
                "message": "Face verification failed. Please try again.",
                "user_id": user_id,
                "confidence": 0.0
            }
        
    except Exception as e:
        print(f"❌ Error verifying face: {e}")
        raise HTTPException(status_code=500, detail=f"Error verifying face: {str(e)}")

# ============================================================================
# 3. LOCKER UNLOCK API (Simple version)
# ============================================================================

@router.post("/unlock-locker")
async def unlock_locker_with_face(
    file: UploadFile = File(...),
    locker_id: str = Form(...),
    user_id: str = Form("owner"),  # Default to "owner" for demo
):
    """
    Unlock locker using face recognition (Simple version)
    """
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image data
        image_data = await file.read()
        
        # Check if user has registered face
        if user_id not in REGISTERED_FACES:
            raise HTTPException(status_code=400, detail="No face registered for this user. Please register your face first.")
        
        # Simple verification (always return success for demo)
        # In real implementation, you would compare face encodings here
        is_match = True  # Demo: always match
        
        if is_match:
            print(f"🔓 Locker {locker_id} unlocked successfully for user: {user_id}")
            return {
                "success": True,
                "message": f"Locker {locker_id} unlocked successfully! Welcome back.",
                "user_id": user_id,
                "locker_id": locker_id,
                "confidence": 0.95
            }
        else:
            print(f"❌ Face verification failed for locker {locker_id}, user: {user_id}")
            return {
                "success": False,
                "message": "Face verification failed. Cannot unlock locker. Please try again.",
                "user_id": user_id,
                "locker_id": locker_id,
                "confidence": 0.0
            }
        
    except Exception as e:
        print(f"❌ Error unlocking locker: {e}")
        raise HTTPException(status_code=500, detail=f"Error unlocking locker: {str(e)}")

# ============================================================================
# 4. UTILITY APIs
# ============================================================================

@router.get("/status")
async def face_recognition_status():
    """Check if face recognition service is working"""
    return {
        "status": "healthy",
        "service": "Face Recognition API (Simple Demo)",
        "face_images_dir": FACE_IMAGES_DIR,
        "available": os.path.exists(FACE_IMAGES_DIR),
        "registered_users": list(REGISTERED_FACES.keys()),
        "endpoints": {
            "register": "/register - Register user face",
            "verify": "/verify - Verify user face", 
            "unlock": "/unlock-locker - Unlock locker with face"
        }
    }

@router.delete("/unregister")
async def unregister_face(
    user_id: str = "owner",  # Default to "owner" for demo
):
    """Remove user's registered face"""
    
    if user_id not in REGISTERED_FACES:
        raise HTTPException(status_code=400, detail="No face registered for this user")
    
    try:
        # Remove from memory
        del REGISTERED_FACES[user_id]
        
        print(f"🗑️ Face registration removed for user: {user_id}")
        
        return {
            "success": True,
            "message": "Face registration removed successfully",
            "user_id": user_id
        }
        
    except Exception as e:
        print(f"❌ Error removing face registration: {e}")
        raise HTTPException(status_code=500, detail=f"Error removing face registration: {str(e)}") 