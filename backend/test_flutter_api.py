#!/usr/bin/env python3
"""
Test script to simulate Flutter app API calls
"""

import requests
import json
import time
import os

# API Configuration
BASE_URL = "http://localhost:8000/api/face"

def test_register_face():
    """Test face registration like Flutter app"""
    print("📱 Testing Face Registration (Flutter App Simulation)")
    print("=" * 50)
    
    # Create a dummy image file for testing
    dummy_image_path = "test_face.jpg"
    
    # Create a simple test image (1x1 pixel JPEG)
    test_image_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
    
    with open(dummy_image_path, 'wb') as f:
        f.write(test_image_data)
    
    try:
        # Create multipart request like Flutter app
        with open(dummy_image_path, 'rb') as f:
            files = {'file': ('face.jpg', f, 'image/jpeg')}
            data = {'user_id': 'owner'}
            
            print("📤 Sending face registration request...")
            response = requests.post(f"{BASE_URL}/register", files=files, data=data)
            
            print(f"📥 Response status: {response.status_code}")
            print(f"📥 Response: {response.json()}")
            
            if response.status_code == 200 and response.json().get('success'):
                print("✅ Face registration successful!")
                return True
            else:
                print("❌ Face registration failed!")
                return False
                
    except Exception as e:
        print(f"❌ Error in face registration: {e}")
        return False
    finally:
        # Clean up test file
        if os.path.exists(dummy_image_path):
            os.remove(dummy_image_path)

def test_unlock_locker():
    """Test locker unlock like Flutter app"""
    print("\n🔓 Testing Locker Unlock (Flutter App Simulation)")
    print("=" * 50)
    
    # Create a dummy image file for testing
    dummy_image_path = "test_face.jpg"
    
    # Create a simple test image (1x1 pixel JPEG)
    test_image_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
    
    with open(dummy_image_path, 'wb') as f:
        f.write(test_image_data)
    
    try:
        # Create multipart request like Flutter app
        with open(dummy_image_path, 'rb') as f:
            files = {'file': ('face.jpg', f, 'image/jpeg')}
            data = {
                'user_id': 'owner',
                'locker_id': '12'
            }
            
            print("📤 Sending locker unlock request...")
            response = requests.post(f"{BASE_URL}/unlock-locker", files=files, data=data)
            
            print(f"📥 Response status: {response.status_code}")
            print(f"📥 Response: {response.json()}")
            
            if response.status_code == 200 and response.json().get('success'):
                print("✅ Locker unlock successful!")
                print("🔓 FACE MATCH DETECTED - Locker unlocked successfully!")
                return True
            else:
                print("❌ Locker unlock failed!")
                return False
                
    except Exception as e:
        print(f"❌ Error in locker unlock: {e}")
        return False
    finally:
        # Clean up test file
        if os.path.exists(dummy_image_path):
            os.remove(dummy_image_path)

def main():
    """Run all Flutter app simulation tests"""
    print("🧪 Testing Smart Locker APIs (Flutter App Simulation)")
    print("=" * 60)
    
    # Test 1: Register face
    print("\n1️⃣ Testing Face Registration...")
    register_success = test_register_face()
    
    # Test 2: Unlock locker
    print("\n2️⃣ Testing Locker Unlock...")
    unlock_success = test_unlock_locker()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"   Face Registration: {'✅ PASS' if register_success else '❌ FAIL'}")
    print(f"   Locker Unlock: {'✅ PASS' if unlock_success else '❌ FAIL'}")
    
    if register_success and unlock_success:
        print("\n🎉 All tests passed! The API is working correctly.")
        print("📱 Flutter app should work with this backend.")
    else:
        print("\n⚠️  Some tests failed. Check the API implementation.")
    
    print("\n🔍 Backend logs should show:")
    print("   ✅ Face registered successfully for user: owner")
    print("   🔓 Locker 12 unlocked successfully for user: owner")

if __name__ == "__main__":
    main() 