# 🚀 Hướng dẫn Tạo Repository và Push Code

## 📋 Bước 1: Tạo Repository trên GitHub

### 1.1 Vào GitHub
- Mở trình duyệt và vào: https://github.com
- Đăng nhập vào tài khoản của bạn

### 1.2 Tạo Repository mới
- Click nút "New" hoặc "+" (góc trên bên phải)
- Điền thông tin:
  - **Repository name**: `lock_id` hoặc `smart-locker-system`
  - **Description**: `Smart Locker System with Face Recognition`
  - **Visibility**: Chọn Public hoặc Private
  - **KHÔNG** check "Add a README file"
  - **KHÔNG** check "Add .gitignore"
  - **KHÔNG** check "Choose a license"
- Click "Create repository"

## 📋 Bước 2: Cấu hình Git

### 2.1 Xóa remote cũ
```bash
git remote remove origin
```

### 2.2 Thêm remote mới (chọn 1 trong 3 options)

#### Option A: HTTPS với Username
```bash
git remote add origin https://Quynhdz19@github.com/Quynhdz19/lock_id.git
```

#### Option B: HTTPS với Personal Access Token
```bash
# Tạo Personal Access Token:
# 1. Vào GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
# 2. Generate new token
# 3. Chọn scopes: repo, workflow
# 4. Copy token và sử dụng:
git remote add origin https://YOUR_TOKEN@github.com/Quynhdz19/lock_id.git
```

#### Option C: SSH (nếu có SSH key)
```bash
git remote add origin git@github.com:Quynhdz19/lock_id.git
```

## 📋 Bước 3: Push Code

```bash
# Kiểm tra remote
git remote -v

# Push code
git push -u origin main
```

## 🔧 Troubleshooting

### Lỗi Permission Denied
```bash
# Tạo Personal Access Token mới
# 1. Vào GitHub Settings > Developer settings > Personal access tokens
# 2. Generate new token (classic)
# 3. Chọn scopes: repo (full control)
# 4. Copy token
# 5. Sử dụng token:
git remote set-url origin https://YOUR_TOKEN@github.com/Quynhdz19/lock_id.git
git push -u origin main
```

### Lỗi Repository Not Found
```bash
# Đảm bảo repository đã được tạo trên GitHub
# Kiểm tra URL repository
git remote -v

# Tạo repository mới nếu cần
git remote set-url origin https://github.com/Quynhdz19/new-repo-name.git
```

### Lỗi SSH Key
```bash
# Kiểm tra SSH key
ls -la ~/.ssh

# Tạo SSH key mới nếu cần
ssh-keygen -t ed25519 -C "your_email@example.com"

# Thêm SSH key vào GitHub
# 1. Copy public key: cat ~/.ssh/id_ed25519.pub
# 2. Vào GitHub Settings > SSH and GPG keys
# 3. Add new SSH key
```

## 📁 Files sẽ được push

```
lock_id/
├── backend/
│   ├── main_simple.py              # FastAPI server
│   ├── api/routes/face_recognition_simple.py  # Face APIs
│   ├── requirements_simple.txt      # Dependencies
│   └── test_flutter_api.py         # Test script
├── frontend/locker_app/
│   └── lib/main.dart               # Flutter app
├── README.md                       # Documentation
├── PROJECT_SUMMARY.md              # Project summary
├── GITHUB_SETUP.md                # GitHub guide
├── .gitignore                     # Git ignore
└── push_to_github.sh              # Push script
```

## 🎯 Tính năng chính

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

Nếu vẫn gặp vấn đề:
1. Kiểm tra GitHub account permissions
2. Tạo repository với tên khác
3. Sử dụng Personal Access Token mới
4. Kiểm tra SSH key nếu dùng SSH

**Chúc bạn thành công! 🚀** 