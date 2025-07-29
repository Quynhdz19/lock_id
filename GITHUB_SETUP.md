# 🚀 Hướng dẫn Push Code lên GitHub

## 📋 Bước 1: Tạo Repository trên GitHub

1. **Vào GitHub**: https://github.com
2. **Đăng nhập** vào tài khoản của bạn
3. **Tạo repository mới**:
   - Click "New" hoặc "+" button
   - Đặt tên: `lock_id` hoặc `smart-locker-system`
   - Chọn "Public" hoặc "Private"
   - **KHÔNG** check "Add a README file"
   - Click "Create repository"

## 📋 Bước 2: Kiểm tra Git Status

```bash
# Kiểm tra trạng thái hiện tại
git status

# Kiểm tra remote URL
git remote -v
```

## 📋 Bước 3: Cấu hình Remote Repository

### Option 1: Sử dụng HTTPS
```bash
# Xóa remote cũ (nếu có)
git remote remove origin

# Thêm remote mới
git remote add origin https://github.com/Quynhdz19/lock_id.git

# Hoặc tạo repository mới
git remote add origin https://github.com/Quynhdz19/smart-locker-system.git
```

### Option 2: Sử dụng SSH (nếu có SSH key)
```bash
git remote add origin git@github.com:Quynhdz19/lock_id.git
```

## 📋 Bước 4: Push Code

```bash
# Push lên GitHub
git push -u origin main
```

## 🔧 Troubleshooting

### Lỗi Permission Denied
```bash
# Tạo Personal Access Token
# 1. Vào GitHub Settings > Developer settings > Personal access tokens
# 2. Generate new token
# 3. Copy token và sử dụng khi push

git remote set-url origin https://YOUR_TOKEN@github.com/Quynhdz19/lock_id.git
```

### Lỗi Repository Not Found
```bash
# Đảm bảo repository đã được tạo trên GitHub
# Kiểm tra URL repository
git remote -v

# Tạo repository mới nếu cần
git remote set-url origin https://github.com/Quynhdz19/new-repo-name.git
```

## 📁 Files sẽ được push

### Backend Files
- ✅ `backend/main_simple.py` - FastAPI server
- ✅ `backend/api/routes/face_recognition_simple.py` - Face recognition APIs
- ✅ `backend/requirements_simple.txt` - Python dependencies
- ✅ `backend/test_flutter_api.py` - Test script

### Frontend Files
- ✅ `frontend/locker_app/lib/main.dart` - Flutter app
- ✅ `frontend/locker_app/pubspec.yaml` - Flutter dependencies

### Documentation
- ✅ `README.md` - Project documentation
- ✅ `PROJECT_SUMMARY.md` - Comprehensive summary
- ✅ `.gitignore` - Git ignore rules
- ✅ `push_to_github.sh` - Push guide script

## 🎯 Repository sẽ có

```
smart-locker-system/
├── backend/
│   ├── api/routes/
│   │   └── face_recognition_simple.py
│   ├── config/
│   ├── models/
│   ├── main_simple.py
│   ├── requirements_simple.txt
│   └── test_flutter_api.py
├── frontend/locker_app/
│   ├── lib/main.dart
│   └── pubspec.yaml
├── README.md
├── PROJECT_SUMMARY.md
├── .gitignore
└── push_to_github.sh
```

## 📊 Tính năng chính

1. **Face Registration API** - Đăng ký khuôn mặt
2. **Face Verification API** - Xác thực khuôn mặt
3. **Locker Unlock API** - Mở khóa tủ
4. **Flutter Camera Integration** - Chụp ảnh khuôn mặt
5. **Real-time Logging** - Log khi face match
6. **Test Scripts** - Verify functionality

## 🚀 Sau khi push thành công

1. **Clone repository**:
   ```bash
   git clone https://github.com/Quynhdz19/lock_id.git
   ```

2. **Chạy Backend**:
   ```bash
   cd lock_id/backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements_simple.txt
   python main_simple.py
   ```

3. **Chạy Flutter App**:
   ```bash
   cd lock_id/frontend/locker_app
   flutter pub get
   flutter run
   ```

4. **Test API**:
   ```bash
   cd lock_id/backend
   python test_flutter_api.py
   ```

## 🎉 Kết quả mong đợi

- ✅ Repository trên GitHub với đầy đủ code
- ✅ Backend API hoạt động tại localhost:8000
- ✅ Flutter app với camera integration
- ✅ Face recognition system hoạt động
- ✅ Logging khi face match: `✅ FACE MATCH DETECTED`
- ✅ Documentation đầy đủ

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra GitHub token permissions
2. Đảm bảo repository đã được tạo
3. Kiểm tra git remote URL
4. Thử tạo repository với tên khác

**Chúc bạn thành công! 🚀** 