# Hệ thống điểm danh bằng khuôn mặt

### Thêm file .env vào sau đó thay đổi các thông số trong <> để kết nối với MySQL

```dotenv
DB_USER=<username_db>
DB_PASS=<password_db>
DB_HOST=<db_host>
DB_NAME=<db_name>
```

### Cài đặt các gói thư viện sử dụng

```commandline
pip install -r requirements.txt
```

### Chạy sử dụng ứng dụng

```commandline
python main.py
```

### Đã đạt được

- Đã có thể điểm danh cơ bản bằng cách kéo thả ảnh
- Có giao diện cơ bản cho người dùng

### Chưa đạt được và sẽ phát triển

- Chưa có giao diện admin
- Điểm danh qua camera
- Cần CSS giao diện
- Khóa vị trí cần điểm danh
- Tích hợp với phần mềm quản lý sinh viên