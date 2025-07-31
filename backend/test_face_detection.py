#!/usr/bin/env python3
"""
Test script for face detection debugging
"""

import requests
import json
import sys
import os

# API base URL
BASE_URL = "http://localhost:8000"

def test_server_status():
    """Test if server is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print("✅ Server is running")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Server not accessible: {e}")
        return False

def test_debug_image(image_path):
    """Test image processing with debug endpoint"""
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/api/face/test-image", files=files)
        
        print(f"🔍 Debug Image Response:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Image processed successfully")
                print(f"📊 Image shape: {data['image_info']['shape']}")
                print(f"👥 Faces detected: {data['image_info']['faces_detected']}")
                if data['image_info']['faces_detected'] > 0:
                    print(f"📍 Face locations: {data['image_info']['face_locations']}")
                return True
            else:
                print("❌ Image processing failed")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing debug image: {e}")
        return False

def test_face_registration(image_path, user_id="owner"):
    """Test face registration"""
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            data = {'user_id': user_id}
            response = requests.post(f"{BASE_URL}/api/face/register", files=files, data=data)
        
        print(f"🔍 Registration Response:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            print("✅ Face registration successful")
            return True
        else:
            print(f"❌ Registration failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing registration: {e}")
        return False

def main():
    print("🔧 Face Detection Debug Tool")
    print("=" * 40)
    
    # Test server status
    if not test_server_status():
        return
    
    print("\n" + "=" * 40)
    
    # Get image path from command line or use default
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = input("Enter path to your face image: ").strip()
    
    if not image_path:
        print("❌ No image path provided")
        return
    
    print(f"\n📸 Testing with image: {image_path}")
    
    # Test debug endpoint first
    print("\n🔍 Step 1: Testing image processing...")
    if test_debug_image(image_path):
        print("\n🔍 Step 2: Testing face registration...")
        test_face_registration(image_path)
    else:
        print("❌ Image processing failed. Cannot proceed with registration.")

if __name__ == "__main__":
    main() 