# Face Recognition API Documentation

## Overview
This API provides face recognition capabilities for the locker management system. It includes two main functionalities:
1. **Face Registration** - Register user's face for authentication
2. **Face Verification** - Verify user's face to unlock lockers

## Base URL
```
http://localhost:8000/face-recognition
```

## Authentication
All endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

## 1. Face Registration API

### Register User Face
**POST** `/register`

Register a user's face for future authentication.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Image file (JPG, PNG, etc.)

**Response:**
```json
{
  "success": true,
  "message": "Face registered successfully! You can now use face recognition to unlock your locker.",
  "user_id": 1,
  "face_image_path": "user_1_abc123.jpg"
}
```

**Error Responses:**
- `400` - No face detected in image
- `400` - Invalid file type
- `500` - Server error

---

## 2. Face Verification API

### Verify User Face
**POST** `/verify`

Verify if the uploaded face image matches the registered face.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Image file (JPG, PNG, etc.)

**Response (Success):**
```json
{
  "success": true,
  "message": "Face verification successful! Identity confirmed.",
  "user_id": 1,
  "confidence": 0.95
}
```

**Response (Failure):**
```json
{
  "success": false,
  "message": "Face verification failed. Please try again.",
  "user_id": 1,
  "confidence": 0.0
}
```

**Error Responses:**
- `400` - No face detected in image
- `400` - No face registered for user
- `400` - Registered face image not found
- `500` - Server error

---

## 3. Locker Unlock API

### Unlock Locker with Face
**POST** `/unlock-locker`

Combines face verification with locker unlocking.

**Request:**
- Content-Type: `multipart/form-data`
- Body: 
  - Image file (JPG, PNG, etc.)
  - `locker_id`: String (form field)

**Response (Success):**
```json
{
  "success": true,
  "message": "Locker A12 unlocked successfully! Welcome back.",
  "user_id": 1,
  "locker_id": "A12"
}
```

**Response (Failure):**
```json
{
  "success": false,
  "message": "Face verification failed. Cannot unlock locker. Please try again.",
  "user_id": 1
}
```

---

## 4. Utility APIs

### Check API Status
**GET** `/status`

Check if the face recognition service is working.

**Response:**
```json
{
  "status": "healthy",
  "service": "Face Recognition API",
  "face_images_dir": "face_recognition/data/faces",
  "available": true,
  "endpoints": {
    "register": "/register - Register user face",
    "verify": "/verify - Verify user face",
    "unlock": "/unlock-locker - Unlock locker with face"
  }
}
```

### Remove Face Registration
**DELETE** `/unregister`

Remove user's registered face.

**Response:**
```json
{
  "success": true,
  "message": "Face registration removed successfully",
  "user_id": 1
}
```

---

## Usage Examples

### Using cURL

**Register Face:**
```bash
curl -X POST "http://localhost:8000/face-recognition/register" \
  -H "Authorization: Bearer <your_token>" \
  -F "file=@face_image.jpg"
```

**Verify Face:**
```bash
curl -X POST "http://localhost:8000/face-recognition/verify" \
  -H "Authorization: Bearer <your_token>" \
  -F "file=@face_image.jpg"
```

**Unlock Locker:**
```bash
curl -X POST "http://localhost:8000/face-recognition/unlock-locker" \
  -H "Authorization: Bearer <your_token>" \
  -F "file=@face_image.jpg" \
  -F "locker_id=A12"
```

### Using Python

```python
import requests

# Register face
with open('face.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/face-recognition/register',
        headers={'Authorization': 'Bearer <your_token>'},
        files=files
    )

# Verify face
with open('face.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/face-recognition/verify',
        headers={'Authorization': 'Bearer <your_token>'},
        files=files
    )

# Unlock locker
with open('face.jpg', 'rb') as f:
    files = {'file': f}
    data = {'locker_id': 'A12'}
    response = requests.post(
        'http://localhost:8000/face-recognition/unlock-locker',
        headers={'Authorization': 'Bearer <your_token>'},
        files=files,
        data=data
    )
```

---

## Technical Details

### Face Detection
- Uses `face_recognition` library
- Detects faces using HOG (Histogram of Oriented Gradients)
- Supports multiple face formats (JPG, PNG, etc.)

### Face Encoding
- Converts faces to 128-dimensional feature vectors
- Uses deep learning model for feature extraction
- Tolerant to lighting and angle variations

### Verification Tolerance
- Default tolerance: 0.6 (60% similarity required)
- Lower tolerance = stricter matching
- Higher tolerance = more lenient matching

### Image Storage
- Face images stored in `face_recognition/data/faces/`
- Filename format: `user_{user_id}_{uuid}.jpg`
- Automatic cleanup of old images when re-registering

---

## Error Handling

### Common Issues

1. **No face detected**
   - Ensure face is clearly visible
   - Check lighting conditions
   - Try different angles

2. **Face verification failed**
   - Ensure same person in both images
   - Check image quality
   - Try re-registering face

3. **Permission errors**
   - Check file permissions
   - Ensure directory exists
   - Verify user authentication

### Debugging

Enable debug logging by setting environment variable:
```bash
export LOG_LEVEL=DEBUG
```

---

## Security Considerations

1. **Image Storage**
   - Images stored locally on server
   - Consider encryption for sensitive data
   - Regular cleanup of unused images

2. **Authentication**
   - JWT tokens required for all endpoints
   - Tokens expire for security
   - Rate limiting recommended

3. **Face Data**
   - Face encodings are mathematical representations
   - Cannot be reverse-engineered to original image
   - Consider GDPR compliance for EU users

---

## Performance

### Response Times
- Face registration: ~2-3 seconds
- Face verification: ~1-2 seconds
- Locker unlock: ~2-3 seconds

### Optimization Tips
- Use appropriate image sizes (640x480 recommended)
- Compress images before upload
- Cache face encodings if possible
- Use SSD storage for faster I/O 