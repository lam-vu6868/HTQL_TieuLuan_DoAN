"""API đăng nhập và thông tin tài khoản.

1. POST /auth/login: nhận LoginRequest, kiểm tra mật khẩu, trả TokenResponse.
2. GET /auth/me: dùng get_current_user(), trả CurrentUserResponse.
3. Trả lỗi xác thực thống nhất; không tiết lộ tài khoản hay mật khẩu sai ở bước nào.
"""
