"""Gói lớp nghiệp vụ.

1. Đặt kiểm tra quyền và chuyển trạng thái ở service, không đặt ở router.
2. Viết async def cho thao tác gọi repository; await truy vấn và commit()/rollback().
3. Mỗi request dùng một AsyncSession, không chạy nhiều thao tác đồng thời trên cùng session.
"""
