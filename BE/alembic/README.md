# Migration PostgreSQL

Sau khi chạy `docker compose up -d postgres` và cài `BE/requirements.txt`, chạy từ thư mục gốc:

```powershell
.\BE\venv\Scripts\python.exe -m alembic -c BE\alembic.ini upgrade head
```

Migration đầu tiên tạo 14 bảng trong `Docs/04-thiet-ke-co-so-du-lieu.md`. Không chạy `downgrade` trên database có dữ liệu vì thao tác này xóa bảng.
