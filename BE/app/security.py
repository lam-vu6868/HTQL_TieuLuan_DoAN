"""Mật khẩu, JWT và người dùng hiện tại.

1. Viết hash_password() và verify_password(); không lưu mật khẩu gốc.
2. Viết create_access_token() và decode_access_token() với hạn dùng rõ ràng.
3. Viết async def get_current_user() nếu cần await truy vấn tài khoản; từ chối token sai/hết hạn.
4. Hàm băm mật khẩu là tác vụ CPU; chạy qua thread khi gọi từ endpoint async nếu chậm.
5. Tạo token đặt lại mật khẩu ngẫu nhiên, chỉ lưu mã băm và thời hạn; xóa sau khi dùng.
6. Quyền theo lớp, nhóm hoặc hồ sơ kiểm tra thêm trong service tương ứng.
"""
