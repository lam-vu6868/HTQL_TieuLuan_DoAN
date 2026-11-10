# HTTT07 — Quản lý đề tài Tiểu luận và Đồ án tốt nghiệp

Bản khởi tạo chặng 1 dùng **ReactJS + Vite**, **FastAPI + Python** và **PostgreSQL local**. Màn hình kiểm tra gọi FastAPI rồi yêu cầu backend thực hiện truy vấn `SELECT 1` trên PostgreSQL.

## 1. Chuẩn bị

- Python 3.12. Nếu dùng Python 3.11, thay `py -3.12` bằng `py -3.11` ở bước tạo môi trường.
- Node.js 22.12 trở lên và npm.
- Dịch vụ PostgreSQL trên máy đang chạy. Dùng cổng và tài khoản PostgreSQL hiện có.

Trong pgAdmin, mở **Query Tool** trên database `postgres` và chạy lệnh dưới đây một lần nếu chưa có database `httt07`.

```sql
CREATE DATABASE httt07;
```

## 2. Chạy backend

Mở PowerShell tại thư mục gốc dự án và chạy:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Mở `backend/.env` và điền tài khoản, mật khẩu, cổng PostgreSQL của máy vào `DATABASE_URL`. File mẫu dùng tài khoản `postgres`, cổng `5432` và database `httt07`. Với mật khẩu có ký tự đặc biệt trong URL, dùng dạng mã hóa tương ứng, ví dụ `@` thành `%40` và `#` thành `%23`. [Cách viết URL kết nối SQLAlchemy](https://docs.sqlalchemy.org/en/20/core/engines.html#escaping-special-characters-such-as-signs-in-passwords)

Chạy FastAPI trong cùng cửa sổ PowerShell:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## 3. Chạy frontend

Mở PowerShell thứ hai tại thư mục gốc dự án và chạy:

```powershell
cd frontend
npm.cmd ci
npm.cmd run dev
```

Mở [màn hình kiểm tra tại cổng 5173](http://127.0.0.1:5173). Khi cả hai thẻ hiện **Đã kết nối**, React đã nhận phản hồi FastAPI và backend đã truy vấn được PostgreSQL.

| Trạng thái | Cách kiểm tra |
| --- | --- |
| FastAPI chưa kết nối | Xem cửa sổ chạy backend và mở [Swagger tại cổng 8000](http://127.0.0.1:8000/docs). |
| FastAPI đã kết nối, PostgreSQL chưa kết nối | Kiểm tra dịch vụ PostgreSQL và tài khoản, mật khẩu, cổng, tên database trong `backend/.env`. Khởi động lại FastAPI nếu đã sửa file này. |

## 4. Cấu trúc hiện tại

| Phần | Trách nhiệm |
| --- | --- |
| `backend/app/config.py` | Lớp `Settings` đọc cấu hình. |
| `backend/app/database.py` | Lớp `Database` quản lý kết nối và truy vấn kiểm tra. |
| `backend/app/main.py` | Khởi tạo FastAPI và cung cấp hai endpoint kiểm tra. |
| `frontend/src/App.jsx` | Gọi hai endpoint và hiển thị riêng trạng thái API, cơ sở dữ liệu. |
| `docs/` | [Nghiệp vụ](docs/01-phan-tich-nghiep-vu.md), [PlantUML](docs/02-so-do-uml.md) và [kế hoạch triển khai](docs/03-ke-hoach-trien-khai.md). |

Bước tiếp theo của chặng 1 là chốt ERD và migration nền. Đăng nhập JWT và phân quyền thuộc chặng 2.
