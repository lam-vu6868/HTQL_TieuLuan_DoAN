"""API đăng nhập và thông tin tài khoản.

1. Viết async def login() cho POST /auth/login: await truy vấn tài khoản, kiểm tra mật khẩu, trả token.
2. Viết async def me() cho GET /auth/me: await get_current_user(), trả CurrentUserResponse.
3. Trả lỗi xác thực thống nhất; không tiết lộ tài khoản hay mật khẩu sai ở bước nào.
"""
