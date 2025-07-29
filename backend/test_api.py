#!/usr/bin/env python3
"""
Test script for Smart Locker Face Recognition APIs
"""

import requests
import json
import time

# API Configuration
BASE_URL = "http://localhost:8000/api/face"

def test_health():
    """Test if server is running"""
    try:
        response = requests.get(f"{BASE_URL}/status")
        print(f"✅ Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_register_face(image_path):
    """Test face registration"""
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            data = {'user_id': 'owner'}
            
            response = requests.post(f"{BASE_URL}/register", files=files, data=data)
            
            print(f"🔍 Register response: {response.status_code}")
            print(f"Response: {response.json()}")
            
            return response.status_code == 200 and response.json().get('success', False)
    except Exception as e:
        print(f"❌ Register test failed: {e}")
        return False

def test_verify_face(image_path):
    """Test face verification"""
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            data = {'user_id': 'owner'}
            
            response = requests.post(f"{BASE_URL}/verify", files=files, data=data)
            
            print(f"🔍 Verify response: {response.status_code}")
            print(f"Response: {response.json()}")
            
            return response.status_code == 200 and response.json().get('success', False)
    except Exception as e:
        print(f"❌ Verify test failed: {e}")
        return False

def test_unlock_locker(image_path, locker_id="12"):
    """Test locker unlock"""
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            data = {
                'user_id': 'owner',
                'locker_id': locker_id
            }
            
            response = requests.post(f"{BASE_URL}/unlock-locker", files=files, data=data)
            
            print(f"🔍 Unlock response: {response.status_code}")
            print(f"Response: {response.json()}")
            
            return response.status_code == 200 and response.json().get('success', False)
    except Exception as e:
        print(f"❌ Unlock test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Smart Locker Face Recognition APIs")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1️⃣ Testing health check...")
    if not test_health():
        print("❌ Server not running. Please start the backend first.")
        return
    
    # Test 2: Register face (requires image file)
    print("\n2️⃣ Testing face registration...")
    print("📝 Note: This test requires a face image file.")
    print("   Create a test image or use an existing one.")
    
    # You can uncomment and modify this to test with actual image
    # image_path = "test_face.jpg"  # Replace with your image path
    # if test_register_face(image_path):
    #     print("✅ Face registration successful!")
    # else:
    #     print("❌ Face registration failed!")
    
    print("⏭️  Skipping face registration test (no image provided)")
    
    # Test 3: Verify face
    print("\n3️⃣ Testing face verification...")
    print("📝 Note: This test requires a face image file.")
    print("   Create a test image or use an existing one.")
    
    # You can uncomment and modify this to test with actual image
    # if test_verify_face(image_path):
    #     print("✅ Face verification successful!")
    # else:
    #     print("❌ Face verification failed!")
    
    print("⏭️  Skipping face verification test (no image provided)")
    
    # Test 4: Unlock locker
    print("\n4️⃣ Testing locker unlock...")
    print("📝 Note: This test requires a face image file.")
    print("   Create a test image or use an existing one.")
    
    # You can uncomment and modify this to test with actual image
    # if test_unlock_locker(image_path):
    #     print("✅ Locker unlock successful!")
    # else:
    #     print("❌ Locker unlock failed!")
    
    print("⏭️  Skipping locker unlock test (no image provided)")
    
    print("\n✅ API tests completed!")
    print("\n📱 To test with Flutter app:")
    print("   1. Start the backend: python run_server.py")
    print("   2. Run Flutter app: flutter run")
    print("   3. Use the app to register and verify faces")

if __name__ == "__main__":
    main() 