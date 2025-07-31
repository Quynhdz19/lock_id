# Face Detection Testing Guide

## Problem
You're getting the error: `"No face detected in image. Please ensure your face is clearly visible."`

## Solution Steps

### 1. Test with Your Own Image
The existing test image is very small (1x1 pixel) and won't work for face detection. You need to use a real photo of your face.

### 2. Prepare Your Image
- Take a clear photo of your face
- Make sure your face is clearly visible and well-lit
- Save it as JPG or PNG format
- The image should be at least 100x100 pixels

### 3. Test the Image Processing
Run this command with your image path:
```bash
source venv/bin/activate
python test_with_real_image.py /path/to/your/face/image.jpg
```

### 4. Test Face Registration
If the image processing works, test face registration:
```bash
curl -X POST http://localhost:8000/api/face/register \
  -F "file=@/path/to/your/face/image.jpg" \
  -F "user_id=owner"
```

### 5. Common Issues and Solutions

#### Issue: "File must be an image"
- Make sure the file is actually an image (JPG, PNG, etc.)
- Check that the file path is correct
- Ensure the file is not corrupted

#### Issue: "No face detected in image"
- Make sure your face is clearly visible in the image
- Ensure good lighting
- Try a different angle or closer shot
- Make sure the image is not too small (at least 100x100 pixels)

#### Issue: "Could not decode image"
- Check if the image file is corrupted
- Try a different image format
- Make sure the file is actually an image file

### 6. Debug Information
The server now provides detailed debugging information:
- ✅ Image decoded successfully - The image was loaded properly
- 🔍 Found X face(s) in image - Number of faces detected
- ✅ Successfully encoded X face(s) - Number of faces encoded
- ❌ No faces detected in image - No faces found in the image

### 7. Example Test
```bash
# Test with a real image
python test_with_real_image.py ~/Desktop/my_face.jpg

# If successful, register the face
curl -X POST http://localhost:8000/api/face/register \
  -F "file=@~/Desktop/my_face.jpg" \
  -F "user_id=owner"
```

## Server Status
The server is running at: http://localhost:8000

Check server status:
```bash
curl http://localhost:8000/health
```

## API Endpoints
- `/api/face/register` - Register your face
- `/api/face/verify` - Verify your face
- `/api/face/test-image` - Test image processing
- `/health` - Check server status 