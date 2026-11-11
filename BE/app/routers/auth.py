"""API đăng nhập và thông tin tài khoản.

1. Viết async def login() cho POST /auth/login: await truy vấn tài khoản, kiểm tra mật khẩu, trả token.
2. Viết async def me() cho GET /auth/me: await get_current_user(), trả CurrentUserResponse.
3. Viết async def request_password_reset()/confirm_password_reset(); gọi AuthService, không gửi email trực tiếp trong router.
4. Trả phản hồi yêu cầu reset như nhau dù email tồn tại hay không; token hết hạn hoặc đã dùng phải bị từ chối.
"""
