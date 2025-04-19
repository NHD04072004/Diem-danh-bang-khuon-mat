# Hệ thống điểm danh bằng khuôn mặt

## Tổng quan về hệ thống

Hệ thống điểm danh bằng khuôn mặt, người dùng sẽ đưa ảnh có khuôn mặt vào sau đó ấn nút điểm danh, sau đó hệ thống sẽ lưu vào cơ sở dữ liệu. Mỗi người dùng chỉ được điểm danh một lần duy nhất trong một buổi học của khóa học.

## Các chức năng chính

### Admin 

- Thêm, sửa, xóa người dùng
- Thêm, sửa, xóa khóa học
- Xem điểm danh

### User

- Xem khóa học
- Đăng ký vào khóa học
- Điểm danh

## Cài đặt và triển khai

**Yêu cầu**

- Cài đặt Python: https://www.python.org/downloads/
- Cài đặt MySQL: https://dev.mysql.com/downloads/

**Clone source code về máy tính**

```commandline
git clone https://github.com/NHD04072004/Diem-danh-bang-khuon-mat.git
```

**Thêm file `.env` vào sau đó thay đổi các thông số trong <> để kết nối với MySQL**

```dotenv
DB_USER=<username_db>
DB_PASS=<password_db>
DB_HOST=<db_host>
DB_NAME=<db_name>
```

**Cài đặt các gói thư viện sử dụng**

```commandline
pip install -r requirements.txt
```

**Chạy sử dụng ứng dụng**

```commandline
python main.py
```
