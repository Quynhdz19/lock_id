# Smart Locker Backend API

Backend API cho hệ thống Smart Locker tích hợp AI Face Recognition.

## Tính năng

- **Authentication**: Đăng ký, đăng nhập với JWT
- **Face Recognition**: Nhận diện khuôn mặt sử dụng thư viện face_recognition
- **Locker Management**: Quản lý tủ khóa, mở/khóa tủ
- **Access Control**: Kiểm soát truy cập dựa trên nhận diện khuôn mặt
- **Logging**: Ghi log tất cả hoạt động truy cập

## Cài đặt

1. Tạo virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows
```

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

3. Chạy server:
```bash
python main.py
```

Server sẽ chạy tại `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Đăng ký user mới
- `POST /api/auth/token` - Đăng nhập và lấy JWT token
- `GET /api/auth/me` - Lấy thông tin user hiện tại

### Face Recognition
- `POST /api/face/register` - Đăng ký khuôn mặt cho user
- `POST /api/face/verify` - Xác thực khuôn mặt
- `POST /api/face/verify-and-unlock` - Xác thực và mở khóa tủ
- `GET /api/face/users/{user_id}/face` - Lấy thông tin face data
- `DELETE /api/face/users/{user_id}/face` - Xóa face data
- `GET /api/face/access-logs` - Lấy log truy cập

### Locker Management
- `GET /api/locker/` - Lấy danh sách tất cả tủ
- `GET /api/locker/{locker_id}` - Lấy thông tin tủ cụ thể
- `POST /api/locker/` - Tạo tủ mới
- `PUT /api/locker/{locker_id}/lock` - Khóa tủ
- `PUT /api/locker/{locker_id}/unlock` - Mở khóa tủ
- `PUT /api/locker/{locker_id}/assign` - Gán tủ cho user
- `PUT /api/locker/{locker_id}/release` - Giải phóng tủ
- `GET /api/locker/status/overview` - Tổng quan trạng thái tủ

## Cấu trúc Database

- **users**: Thông tin người dùng
- **face_data**: Dữ liệu khuôn mặt đã mã hóa
- **lockers**: Thông tin tủ khóa
- **access_logs**: Log truy cập

## Tích hợp Hardware

Để tích hợp với phần cứng thực tế, cần implement các TODO trong:
- `api/routes/locker.py` - Điều khiển khóa tủ
- `api/routes/face_recognition.py` - Tích hợp camera

## Bảo mật

- Sử dụng JWT cho authentication
- Mã hóa password với bcrypt
- Face recognition với confidence threshold 80%
- Logging tất cả hoạt động truy cập 