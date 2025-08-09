# Hướng dẫn cấu hình Firebase cho Locker App

## Bước 1: Tạo Firebase Project

1. Truy cập [Firebase Console](https://console.firebase.google.com/)
2. Tạo project mới với tên "lock-id-46378"
3. Bật Realtime Database

## Bước 2: Cấu hình Android

### 2.1. Thêm Android App vào Firebase
1. Trong Firebase Console, vào **Project Settings**
2. Chọn tab **General**
3. Scroll xuống phần **Your apps**, click **Add app** → **Android**
4. Nhập thông tin:
   - **Android package name**: `com.example.locker_app`
   - **App nickname**: Locker App
   - **Debug signing certificate SHA-1**: (có thể bỏ qua)
5. Click **Register app**

### 2.2. Tải file google-services.json
1. Tải file `google-services.json` từ Firebase Console
2. Đặt file vào thư mục: `android/app/google-services.json`
3. **QUAN TRỌNG**: Thay thế file template hiện tại bằng file thật từ Firebase

### 2.3. Cấu hình build.gradle
✅ Đã cấu hình sẵn trong `android/app/build.gradle.kts`:
- Thêm plugin `com.google.gms.google-services`
- Thêm dependencies Firebase

## Bước 3: Cấu hình iOS

### 3.1. Thêm iOS App vào Firebase
1. Trong Firebase Console, vào **Project Settings**
2. Click **Add app** → **iOS**
3. Nhập thông tin:
   - **iOS bundle ID**: `com.example.lockerApp`
   - **App nickname**: Locker App iOS
4. Click **Register app**

### 3.2. Tải file GoogleService-Info.plist
1. Tải file `GoogleService-Info.plist` từ Firebase Console
2. Đặt file vào thư mục: `ios/Runner/GoogleService-Info.plist`
3. **QUAN TRỌNG**: Thay thế file template hiện tại bằng file thật từ Firebase

### 3.3. Cấu hình Xcode
1. Mở project trong Xcode: `ios/Runner.xcworkspace`
2. Chọn target **Runner**
3. Trong **Build Phases**, thêm file `GoogleService-Info.plist` vào **Copy Bundle Resources**

## Bước 4: Cấu hình Realtime Database

### 4.1. Tạo Database
1. Trong Firebase Console, vào **Realtime Database**
2. Click **Create Database**
3. Chọn location: **asia-southeast1**
4. Chọn mode: **Start in test mode**

### 4.2. Cấu hình Security Rules
```json
{
  "rules": {
    "lockers": {
      "$lockerId": {
        ".read": true,
        ".write": true
      }
    }
  }
}
```

### 4.3. Tạo dữ liệu mẫu
```json
{
  "lockers": {
    "12": {
      "state": "locked",
      "status": "active",
      "lockerNumber": "A12",
      "lastUnlockTime": "2024-01-01T12:00:00.000Z"
    }
  }
}
```

## Bước 5: Cài đặt dependencies

```bash
flutter pub get
```

## Bước 6: Test ứng dụng

### 6.1. Test Android
```bash
flutter run -d android
```

### 6.2. Test iOS
```bash
flutter run -d ios
```

## Bước 7: Kiểm tra kết nối Firebase

Khi app chạy, bạn sẽ thấy log:
- ✅ Firebase initialized successfully
- 📡 Listening to locker state changes
- ✅ Firebase updated: Locker 12 state changed to unlocked

## Troubleshooting

### Lỗi thường gặp:

1. **"Firebase not initialized"**
   - Kiểm tra file `google-services.json` và `GoogleService-Info.plist`
   - Đảm bảo đã chạy `flutter pub get`

2. **"Permission denied"**
   - Kiểm tra Firebase Security Rules
   - Đảm bảo database URL đúng

3. **"Network error"**
   - Kiểm tra kết nối internet
   - Kiểm tra Firebase project settings

### Debug Firebase:
```dart
// Thêm vào main.dart để debug
FirebaseDatabase.instance.setLoggingEnabled(true);
```

## Cấu trúc Database

App sẽ tự động tạo cấu trúc sau trong Firebase:

```json
{
  "lockers": {
    "12": {
      "state": "unlocked",
      "status": "active", 
      "lockerNumber": "A12",
      "lastUnlockTime": "2024-01-15T10:30:00.000Z"
    }
  }
}
```

## Lưu ý quan trọng

1. **Thay thế file config**: Đảm bảo thay thế file template bằng file thật từ Firebase Console
2. **Security Rules**: Trong production, sử dụng rules bảo mật hơn
3. **API Keys**: Không commit API keys vào git repository
4. **Testing**: Test kỹ trước khi deploy production
