#!/usr/bin/env python3
"""
Script to organize existing face images into user-specific folders
"""

import os
import shutil
import re
from datetime import datetime

# Directory containing face images
FACE_IMAGES_DIR = "face_recognition_local/data/faces"

def extract_user_id_from_filename(filename):
    """Extract user ID from filename like 'user_owner_xxx.jpg'"""
    match = re.match(r'user_(.+?)_', filename)
    if match:
        return match.group(1)
    return None

def organize_existing_images():
    """Organize existing images into user-specific folders"""
    print("🔧 Organizing existing face images...")
    
    if not os.path.exists(FACE_IMAGES_DIR):
        print(f"❌ Directory not found: {FACE_IMAGES_DIR}")
        return
    
    # Get all files in the directory
    files = [f for f in os.listdir(FACE_IMAGES_DIR) if os.path.isfile(os.path.join(FACE_IMAGES_DIR, f))]
    
    print(f"📁 Found {len(files)} files to organize")
    
    organized_count = 0
    skipped_count = 0
    
    for filename in files:
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            continue
            
        # Extract user ID from filename
        user_id = extract_user_id_from_filename(filename)
        
        if not user_id:
            print(f"⚠️  Skipping {filename} - cannot extract user ID")
            skipped_count += 1
            continue
        
        # Create user directory
        user_dir = os.path.join(FACE_IMAGES_DIR, user_id)
        os.makedirs(user_dir, exist_ok=True)
        
        # Move file to user directory
        old_path = os.path.join(FACE_IMAGES_DIR, filename)
        new_filename = f"face_legacy_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        new_path = os.path.join(user_dir, new_filename)
        
        try:
            shutil.move(old_path, new_path)
            print(f"✅ Moved {filename} -> {user_id}/{new_filename}")
            organized_count += 1
        except Exception as e:
            print(f"❌ Error moving {filename}: {e}")
            skipped_count += 1
    
    print(f"\n📊 Organization complete:")
    print(f"   ✅ Organized: {organized_count} files")
    print(f"   ⚠️  Skipped: {skipped_count} files")
    
    # Show final structure
    print(f"\n📁 Final directory structure:")
    for item in os.listdir(FACE_IMAGES_DIR):
        item_path = os.path.join(FACE_IMAGES_DIR, item)
        if os.path.isdir(item_path):
            file_count = len([f for f in os.listdir(item_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))])
            print(f"   📂 {item}/ ({file_count} images)")

if __name__ == "__main__":
    organize_existing_images() 