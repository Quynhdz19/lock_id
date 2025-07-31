#!/usr/bin/env python3
"""
Test script for user-specific folder functionality
"""

import requests
import json
import sys
import os

# API base URL
BASE_URL = "http://localhost:8000"

def test_face_registration(image_path, user_id):
    """Test face registration for a specific user"""
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            data = {'user_id': user_id}
            response = requests.post(f"{BASE_URL}/api/face/register", files=files, data=data)
        
        print(f"🔍 Registration Response for user '{user_id}':")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            print(f"✅ Face registration successful for user: {user_id}")
            return True
        else:
            print(f"❌ Registration failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing registration: {e}")
        return False

def list_user_images(user_id):
    """List all images for a specific user"""
    try:
        response = requests.get(f"{BASE_URL}/api/face/list-images/{user_id}")
        
        print(f"🔍 Images for user '{user_id}':")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            data = response.json()
            print(f"📁 User directory: {data.get('user_directory', 'N/A')}")
            print(f"📊 Total images: {data.get('total_images', 0)}")
            return True
        else:
            print(f"❌ Failed to list images: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error listing images: {e}")
        return False

def main():
    print("🔧 User Folder Test")
    print("=" * 40)
    
    # Get image path and user ID
    if len(sys.argv) > 2:
        image_path = sys.argv[1]
        user_id = sys.argv[2]
    else:
        image_path = input("Enter path to your face image: ").strip()
        user_id = input("Enter user ID: ").strip()
    
    if not image_path or not user_id:
        print("❌ Both image path and user ID are required")
        return
    
    print(f"📸 Testing with image: {image_path}")
    print(f"👤 User ID: {user_id}")
    
    # Test face registration
    print(f"\n🔍 Step 1: Registering face for user '{user_id}'...")
    if test_face_registration(image_path, user_id):
        print(f"\n🔍 Step 2: Listing images for user '{user_id}'...")
        list_user_images(user_id)
    else:
        print("❌ Face registration failed. Cannot proceed.")

if __name__ == "__main__":
    main() 