# Hướng Dẫn Sử Dụng User Folder System

## Tổng Quan
Hệ thống đã được cập nhật để tạo folder riêng cho từng user khi đăng ký khuôn mặt. Mỗi user sẽ có một thư mục riêng chứa tất cả ảnh khuôn mặt của họ.

## Cấu Trúc Thư Mục

```
face_recognition_local/data/faces/
├── owner/                    # Thư mục của user "owner"
│   ├── face_20250731_231151_39009439.jpg
│   ├── face_legacy_20250731_231505_user_owner_xxx.jpg
│   └── ...
├── user123/                  # Thư mục của user "user123"
│   └── face_20250731_231151_39009439.jpg
├── alice/                    # Thư mục của user "alice"
│   └── face_20250731_231336_e76616c6.jpg
├── Quynhlx/                  # Thư mục của user "Quynhlx"
│   └── face_xxx.jpg
└── test_images/              # Thư mục chứa ảnh test
    └── test_xxx.jpg
```

## API Endpoints

### 1. Đăng Ký Khuôn Mặt
```bash
POST /api/face/register
```

**Parameters:**
- `file`: File ảnh khuôn mặt
- `user_id`: ID của user (tự động tạo folder)

**Example:**
```bash
curl -X POST http://localhost:8000/api/face/register \
  -F "file=@/path/to/face/image.jpg" \
  -F "user_id=john_doe"
```

**Response:**
```json
{
  "success": true,
  "message": "Face registered successfully! You can now use face recognition to unlock your locker.",
  "user_id": "john_doe",
  "face_image_path": "face_20250731_231151_39009439.jpg"
}
```

### 2. Liệt Kê Ảnh Của User
```bash
GET /api/face/list-images/{user_id}
```

**Example:**
```bash
curl http://localhost:8000/api/face/list-images/owner
```

**Response:**
```json
{
  "user_id": "owner",
  "user_directory": "face_recognition_local/data/faces/owner",
  "total_images": 6,
  "images": [
    {
      "filename": "face_20250731_231151_39009439.jpg",
      "file_path": "face_recognition_local/data/faces/owner/face_20250731_231151_39009439.jpg",
      "file_size": 3814,
      "created_time": "2025-07-31T23:11:51.263134",
      "modified_time": "2025-07-31T23:11:51.263134"
    }
  ]
}
```

### 3. Test Xử Lý Ảnh
```bash
POST /api/face/test-image
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/face/test-image \
  -F "file=@/path/to/test/image.jpg"
```

## Tính Năng Mới

### ✅ Tự Động Tạo Folder
- Khi user đăng ký lần đầu, hệ thống tự động tạo folder `{user_id}/`
- Tất cả ảnh của user sẽ được lưu trong folder riêng

### ✅ Đặt Tên File Thông Minh
- Format: `face_{timestamp}_{uuid}.jpg`
- Ví dụ: `face_20250731_231151_39009439.jpg`

### ✅ Quản Lý Ảnh Theo User
- Mỗi user có folder riêng
- Dễ dàng backup và quản lý
- Tránh xung đột tên file

### ✅ API Liệt Kê Ảnh
- Xem tất cả ảnh của một user
- Thông tin chi tiết về file (kích thước, thời gian tạo)
- Sắp xếp theo thời gian tạo (mới nhất trước)

## Scripts Hỗ Trợ

### 1. Test User Folder
```bash
python test_user_folders.py /path/to/image.jpg user_id
```

### 2. Tổ Chức File Cũ
```bash
python organize_existing_images.py
```

## Lợi Ích

1. **Tổ Chức Tốt Hơn**: Mỗi user có folder riêng
2. **Dễ Quản Lý**: Dễ dàng backup, restore, xóa user
3. **Bảo Mật**: Ảnh của user được tách biệt
4. **Mở Rộng**: Dễ dàng thêm tính năng mới
5. **Debug**: Dễ dàng tìm và sửa lỗi

## Ví Dụ Sử Dụng

### Đăng Ký User Mới
```bash
# Đăng ký user "john"
curl -X POST http://localhost:8000/api/face/register \
  -F "file=@john_face.jpg" \
  -F "user_id=john"

# Kiểm tra folder được tạo
ls face_recognition_local/data/faces/john/

# Liệt kê ảnh của john
curl http://localhost:8000/api/face/list-images/john
```

### Đăng Ký Nhiều Ảnh Cho Cùng User
```bash
# Đăng ký ảnh thứ 2 cho user "john"
curl -X POST http://localhost:8000/api/face/register \
  -F "file=@john_face2.jpg" \
  -F "user_id=john"

# Kiểm tra có 2 ảnh trong folder
curl http://localhost:8000/api/face/list-images/john
```

## Lưu Ý

1. **Folder Tự Động**: Folder được tạo tự động khi user đăng ký lần đầu
2. **Tên File**: File được đặt tên với timestamp để tránh trùng lặp
3. **Backup**: Nên backup toàn bộ thư mục `face_recognition_local/data/faces/`
4. **Permissions**: Đảm bảo server có quyền tạo thư mục và file 