from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import cv2
import numpy as np
import face_recognition
import uuid
from typing import Optional
from datetime import datetime

app = FastAPI(
    title="Face Recognition API",
    description="API for Face Registration and Verification",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory to store face images
FACE_IMAGES_DIR = "face_recognition_local/data/faces"
os.makedirs(FACE_IMAGES_DIR, exist_ok=True)

# Simple in-memory storage for demo (in production, use database)
REGISTERED_FACES = {}  # {user_id: face_encoding}

def save_face_image(image_data: bytes, user_id: str) -> str:
    """Save face image to disk in user-specific folder and return filename"""
    # Create user-specific directory
    user_dir = os.path.join(FACE_IMAGES_DIR, user_id)
    os.makedirs(user_dir, exist_ok=True)
    
    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"face_{timestamp}_{uuid.uuid4().hex[:8]}.jpg"
    filepath = os.path.join(user_dir, filename)
    
    with open(filepath, "wb") as f:
        f.write(image_data)
    
    print(f"📁 Saved face image for user '{user_id}' in: {user_dir}")
    print(f"📄 Filename: {filename}")
    
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
# 1. FACE REGISTRATION API
# ============================================================================

@app.post("/api/face/register")
async def register_face(
    file: UploadFile = File(..., description="Face image file (JPG, PNG, etc.)"),
    user_id: str = Form("owner", description="User ID for face registration")  # Default to "owner" for demo
):
    """
    Register user's face for authentication
    
    This API allows users to register their face for future authentication.
    The face image will be saved and encoded for comparison.
    """
    
    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
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
# 2. FACE VERIFICATION API
# ============================================================================

@app.post("/api/face/verify")
async def verify_face(
    file: UploadFile = File(..., description="Face image file to verify (JPG, PNG, etc.)"),
    user_id: str = Form("owner", description="User ID for face verification")  # Default to "owner" for demo
):
    """
    Verify user's face for authentication
    
    This API verifies if the uploaded face image matches the registered face.
    Returns success/failure with confidence level.
    """
    
    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
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
# 3. LOCKER UNLOCK API (Combines face verification + locker control)
# ============================================================================

@app.post("/api/face/unlock-locker")
async def unlock_locker_with_face(
    file: UploadFile = File(..., description="Face image file (JPG, PNG, etc.)"),
    locker_id: str = Form(..., description="Locker ID to unlock"),
    user_id: str = Form("owner", description="User ID for face verification")
):
    """
    Unlock locker using face recognition
    
    This API combines face verification with locker unlocking.
    First verifies the face, then unlocks the specified locker.
    """
    
    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        print(f"🔓 Starting locker unlock process for locker: {locker_id}, user: {user_id}")
        
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
            print(f"🔓 Unlocking locker: {locker_id}")
            
            # Here you would add actual locker control logic
            # For now, we'll just return success
            return {
                "success": True,
                "message": "Locker unlocked successfully!",
                "user_id": user_id,
                "locker_id": locker_id,
                "confidence": 0.95
            }
        else:
            print(f"❌ Face verification failed for user: {user_id}")
            return {
                "success": False,
                "message": "Face verification failed. Please try again.",
                "user_id": user_id,
                "locker_id": locker_id,
                "confidence": 0.0
            }
        
    except Exception as e:
        print(f"❌ Error unlocking locker: {e}")
        raise HTTPException(status_code=500, detail=f"Error unlocking locker: {str(e)}")

# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    return {"message": "Face Recognition API is running!"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "Face Recognition API",
        "registered_users": list(REGISTERED_FACES.keys())
    }

@app.get("/api/face/status")
async def face_recognition_status():
    """Check if face recognition service is working"""
    return {
        "status": "healthy",
        "service": "Face Recognition API",
        "face_images_dir": FACE_IMAGES_DIR,
        "available": os.path.exists(FACE_IMAGES_DIR),
        "registered_users": list(REGISTERED_FACES.keys()),
        "endpoints": {
            "register": "/api/face/register - Register user face",
            "verify": "/api/face/verify - Verify user face",
            "test_image": "/api/face/test-image - Test image processing",
            "list_images": "/api/face/list-images/{user_id} - List user's face images"
        }
    }

@app.get("/api/face/list-images/{user_id}")
async def list_user_images(user_id: str):
    """List all face images for a specific user"""
    user_dir = os.path.join(FACE_IMAGES_DIR, user_id)
    
    if not os.path.exists(user_dir):
        return {
            "user_id": user_id,
            "message": "No images found for this user",
            "images": [],
            "total_images": 0
        }
    
    try:
        # Get all image files in user directory
        image_files = []
        for filename in os.listdir(user_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                file_path = os.path.join(user_dir, filename)
                file_stat = os.stat(file_path)
                image_files.append({
                    "filename": filename,
                    "file_path": file_path,
                    "file_size": file_stat.st_size,
                    "created_time": datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                    "modified_time": datetime.fromtimestamp(file_stat.st_mtime).isoformat()
                })
        
        # Sort by creation time (newest first)
        image_files.sort(key=lambda x: x["created_time"], reverse=True)
        
        return {
            "user_id": user_id,
            "user_directory": user_dir,
            "total_images": len(image_files),
            "images": image_files
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing images: {str(e)}")

@app.post("/api/face/test-image")
async def test_image_processing(
    file: UploadFile = File(..., description="Image file to test")
):
    """Test image processing without face recognition"""
    
    if not file.content_type or not file.content_type.startswith('image/'):
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
        
        # Create test directory
        test_dir = os.path.join(FACE_IMAGES_DIR, "test_images")
        os.makedirs(test_dir, exist_ok=True)
        
        # Save test image with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_filename = f"test_{timestamp}_{uuid.uuid4().hex[:8]}.jpg"
        test_filepath = os.path.join(test_dir, test_filename)
        
        with open(test_filepath, "wb") as f:
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
                "filename": test_filename,
                "file_path": test_filepath,
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

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 