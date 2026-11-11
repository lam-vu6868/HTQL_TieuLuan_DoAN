"""Đặt lại mật khẩu qua email.

1. Viết async def AuthService.request_password_reset(email): phản hồi chung dù email có/không; tạo token ngẫu nhiên, chỉ lưu hash và thời hạn.
2. Gửi link về PUBLIC_BASE_URL qua SMTP bằng asyncio.to_thread() để không chặn event loop; không ghi token vào log.
3. Viết async def confirm_password_reset(token, mat_khau_moi): kiểm tra hash, hạn dùng; băm mật khẩu mới và xóa token trong một giao dịch.
4. Giới hạn tần suất yêu cầu; không trả token hoặc thông tin tồn tại tài khoản qua API.
"""
