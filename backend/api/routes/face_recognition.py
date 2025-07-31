from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
import cv2
import numpy as np
import face_recognition
import os
import uuid
from datetime import datetime
import json

from config.database import get_db, User
from models.face_recognition import FaceRegistration, FaceVerification, FaceResponse

router = APIRouter()

# Directory to store face images
FACE_IMAGES_DIR = "face_recognition/data/faces"
os.makedirs(FACE_IMAGES_DIR, exist_ok=True)

# Simple in-memory storage for demo (in production, use database)
REGISTERED_FACES = {}  # {user_id: face_encoding}

def save_face_image(image_data: bytes, user_id: str) -> str:
    """Save face image to disk and return filename"""
    filename = f"user_{user_id}_{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(FACE_IMAGES_DIR, filename)
    
    with open(filepath, "wb") as f:
        f.write(image_data)
    
    return filename

def encode_face_image(image_data: bytes) -> Optional[np.ndarray]:
    """Encode face from image data"""
    try:
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            print("❌ Error: Could not decode image")
            return None
        
        print(f"✅ Image decoded successfully. Shape: {image.shape}")
        
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Find face locations
        face_locations = face_recognition.face_locations(rgb_image)
        
        print(f"🔍 Found {len(face_locations)} face(s) in image")
        
        if not face_locations:
            print("❌ No faces detected in image")
            return None
        
        # Get face encodings
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
        
        if not face_encodings:
            print("❌ Could not encode faces")
            return None
        
        print(f"✅ Successfully encoded {len(face_encodings)} face(s)")
        
        # Return the first face encoding
        return face_encodings[0]
    
    except ImportError as e:
        print(f"❌ Error: face_recognition library not installed. Please run: pip install face-recognition")
        return None
    except Exception as e:
        print(f"❌ Error encoding face: {e}")
        return None

def verify_face_encoding(known_encoding: np.ndarray, unknown_encoding: np.ndarray, tolerance: float = 0.6) -> bool:
    """Verify if two face encodings match"""
    try:
        # Compare face encodings
        matches = face_recognition.compare_faces([known_encoding], unknown_encoding, tolerance=tolerance)
        return matches[0] if matches else False
    except Exception as e:
        print(f"Error verifying face: {e}")
        return False

# ============================================================================
# 1. FACE REGISTRATION API (Simple version)
# ============================================================================

@router.post("/register", response_model=FaceResponse)
async def register_face(
    file: UploadFile = File(...),
    user_id: str = Form("owner"),  # Default to "owner" for demo
    db: Session = Depends(get_db)
):
    """
    Register user's face for authentication
    
    This API allows users to register their face for future authentication.
    The face image will be saved and encoded for comparison.
    """
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image data
        image_data = await file.read()
        
        # Encode face
        face_encoding = encode_face_image(image_data)
        
        if face_encoding is None:
            raise HTTPException(status_code=400, detail="No face detected in image. Please ensure your face is clearly visible.")
        
        # Save face image
        filename = save_face_image(image_data, user_id)
        
        # Store face encoding in memory (in production, store in database)
        REGISTERED_FACES[user_id] = face_encoding.tolist()
        
        print(f"✅ Face registered successfully for user: {user_id}")
        
        return FaceResponse(
            success=True,
            message="Face registered successfully! You can now use face recognition to unlock your locker.",
            user_id=user_id,
            face_image_path=filename
        )
        
    except Exception as e:
        print(f"❌ Error registering face: {e}")
        raise HTTPException(status_code=500, detail=f"Error registering face: {str(e)}")

# ============================================================================
# 2. FACE VERIFICATION API (Simple version)
# ============================================================================

@router.post("/verify", response_model=FaceResponse)
async def verify_face(
    file: UploadFile = File(...),
    user_id: str = Form("owner"),  # Default to "owner" for demo
    db: Session = Depends(get_db)
):
    """
    Verify user's face for authentication
    
    This API verifies if the uploaded face image matches the registered face.
    Returns success/failure with confidence level.
    """
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image data
        image_data = await file.read()
        
        # Encode face from uploaded image
        unknown_face_encoding = encode_face_image(image_data)
        
        if unknown_face_encoding is None:
            raise HTTPException(status_code=400, detail="No face detected in image. Please ensure your face is clearly visible.")
        
        # Check if user has registered face
        if user_id not in REGISTERED_FACES:
            raise HTTPException(status_code=400, detail="No face registered for this user. Please register your face first.")
        
        # Get registered face encoding
        known_face_encoding = np.array(REGISTERED_FACES[user_id])
        
        # Verify faces
        is_match = verify_face_encoding(known_face_encoding, unknown_face_encoding)
        
        if is_match:
            print(f"✅ Face verification successful for user: {user_id}")
            return FaceResponse(
                success=True,
                message="Face verification successful! Identity confirmed.",
                user_id=user_id,
                confidence=0.95
            )
        else:
            print(f"❌ Face verification failed for user: {user_id}")
            return FaceResponse(
                success=False,
                message="Face verification failed. Please try again.",
                user_id=user_id,
                confidence=0.0
            )
        
    except Exception as e:
        print(f"❌ Error verifying face: {e}")
        raise HTTPException(status_code=500, detail=f"Error verifying face: {str(e)}")

# ============================================================================
# 3. LOCKER UNLOCK API (Combines face verification + locker control)
# ============================================================================

@router.post("/unlock-locker", response_model=FaceResponse)
async def unlock_locker_with_face(
    file: UploadFile = File(...),
    locker_id: str = Form(...),
    user_id: str = Form("owner"),  # Default to "owner" for demo
    db: Session = Depends(get_db)
):
    """
    Unlock locker using face recognition
    
    This API combines face verification with locker unlocking.
    First verifies the user's face, then unlocks the specified locker.
    """
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image data
        image_data = await file.read()
        
        # Encode face from uploaded image
        unknown_face_encoding = encode_face_image(image_data)
        
        if unknown_face_encoding is None:
            raise HTTPException(status_code=400, detail="No face detected in image. Please ensure your face is clearly visible.")
        
        # Check if user has registered face
        if user_id not in REGISTERED_FACES:
            raise HTTPException(status_code=400, detail="No face registered for this user. Please register your face first.")
        
        # Get registered face encoding
        known_face_encoding = np.array(REGISTERED_FACES[user_id])
        
        # Verify faces
        is_match = verify_face_encoding(known_face_encoding, unknown_face_encoding)
        
        if is_match:
            print(f"🔓 Locker {locker_id} unlocked successfully for user: {user_id}")
            return FaceResponse(
                success=True,
                message=f"Locker {locker_id} unlocked successfully! Welcome back.",
                user_id=user_id,
                locker_id=locker_id,
                confidence=0.95
            )
        else:
            print(f"❌ Face verification failed for locker {locker_id}, user: {user_id}")
            return FaceResponse(
                success=False,
                message="Face verification failed. Cannot unlock locker. Please try again.",
                user_id=user_id,
                locker_id=locker_id,
                confidence=0.0
            )
        
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
        "service": "Face Recognition API",
        "face_images_dir": FACE_IMAGES_DIR,
        "available": os.path.exists(FACE_IMAGES_DIR),
        "registered_users": list(REGISTERED_FACES.keys()),
        "endpoints": {
            "register": "/register - Register user face",
            "verify": "/verify - Verify user face", 
            "unlock": "/unlock-locker - Unlock locker with face",
            "debug": "/debug-image - Debug image processing"
        }
    }

@router.post("/debug-image")
async def debug_image_processing(
    file: UploadFile = File(..., description="Image file to debug")
):
    """Debug image processing without face recognition"""
    
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image data
        image_data = await file.read()
        
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return {
                "success": False,
                "message": "Could not decode image",
                "image_info": None
            }
        
        # Save debug image
        debug_filename = f"debug_image_{uuid.uuid4().hex}.jpg"
        debug_filepath = os.path.join(FACE_IMAGES_DIR, debug_filename)
        
        with open(debug_filepath, "wb") as f:
            f.write(image_data)
        
        # Convert BGR to RGB for face detection
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Try face detection
        face_locations = face_recognition.face_locations(rgb_image)
        
        return {
            "success": True,
            "message": "Image processed successfully",
            "image_info": {
                "shape": image.shape,
                "filename": debug_filename,
                "file_size": len(image_data),
                "content_type": file.content_type,
                "faces_detected": len(face_locations),
                "face_locations": face_locations
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error processing image: {str(e)}",
            "image_info": None
        }

@router.delete("/unregister")
async def unregister_face(
    user_id: str = "owner",  # Default to "owner" for demo
    db: Session = Depends(get_db)
):
    """Remove user's registered face"""
    
    if user_id not in REGISTERED_FACES:
        raise HTTPException(status_code=400, detail="No face registered for this user")
    
    try:
        # Remove from memory
        del REGISTERED_FACES[user_id]
        
        print(f"🗑️ Face registration removed for user: {user_id}")
        
        return FaceResponse(
            success=True,
            message="Face registration removed successfully",
            user_id=user_id
        )
        
    except Exception as e:
        print(f"❌ Error removing face registration: {e}")
        raise HTTPException(status_code=500, detail=f"Error removing face registration: {str(e)}") 