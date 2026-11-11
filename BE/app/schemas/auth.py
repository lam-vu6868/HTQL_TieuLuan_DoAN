"""Dữ liệu API xác thực.

1. Tạo LoginRequest(ten_dang_nhap, mat_khau).
2. Tạo TokenResponse, CurrentUserResponse, PasswordResetRequest(email) và PasswordResetConfirm(token, mat_khau_moi).
3. Không đặt mat_khau_bam, JWT_SECRET hoặc reset_token_hash trong response; yêu cầu reset luôn trả phản hồi chung.
"""
