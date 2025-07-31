#!/usr/bin/env python3
"""
Simple test script for face detection with real images
"""

import requests
import json
import sys
import os

# API base URL
BASE_URL = "http://localhost:8000"

def test_image_upload(image_path):
    """Test image upload and processing"""
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/api/face/test-image", files=files)
        
        print(f"🔍 Response Status: {response.status_code}")
        print(f"🔍 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Image processed successfully")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🔧 Face Detection Test")
    print("=" * 30)
    
    # Get image path
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = input("Enter path to your face image: ").strip()
    
    if not image_path:
        print("❌ No image path provided")
        return
    
    print(f"📸 Testing with: {image_path}")
    
    # Test image processing
    if test_image_upload(image_path):
        print("\n✅ Image processing successful!")
        print("Now you can try face registration with the same image.")
    else:
        print("\n❌ Image processing failed.")
        print("Please check:")
        print("1. The image file exists and is readable")
        print("2. The image contains a clear face")
        print("3. The image format is supported (JPG, PNG, etc.)")

if __name__ == "__main__":
    main() 