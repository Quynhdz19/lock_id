#!/bin/bash

echo "🚀 Bắt đầu cấu hình Firebase cho Locker App..."

# Kiểm tra Flutter
if ! command -v flutter &> /dev/null; then
    echo "❌ Flutter không được tìm thấy. Vui lòng cài đặt Flutter trước."
    exit 1
fi

echo "✅ Flutter đã được cài đặt"

# Cài đặt dependencies
echo "📦 Cài đặt dependencies..."
flutter pub get

# Kiểm tra file config Android
if [ ! -f "android/app/google-services.json" ]; then
    echo "⚠️  File android/app/google-services.json chưa được tạo"
    echo "   Vui lòng tải file từ Firebase Console và đặt vào thư mục android/app/"
else
    echo "✅ File google-services.json đã tồn tại"
fi

# Kiểm tra file config iOS
if [ ! -f "ios/Runner/GoogleService-Info.plist" ]; then
    echo "⚠️  File ios/Runner/GoogleService-Info.plist chưa được tạo"
    echo "   Vui lòng tải file từ Firebase Console và đặt vào thư mục ios/Runner/"
else
    echo "✅ File GoogleService-Info.plist đã tồn tại"
fi

# Cài đặt pods cho iOS
echo "🍎 Cài đặt iOS pods..."
cd ios && pod install && cd ..

echo "✅ Cấu hình Firebase hoàn tất!"
echo ""
echo "📋 Các bước tiếp theo:"
echo "1. Tạo Firebase project tại: https://console.firebase.google.com/"
echo "2. Tải file google-services.json và GoogleService-Info.plist"
echo "3. Đặt file vào đúng thư mục"
echo "4. Chạy: flutter run"
echo ""
echo "📖 Xem hướng dẫn chi tiết tại: FIREBASE_SETUP.md"
