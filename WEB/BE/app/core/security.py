from pwdlib import PasswordHash


# ================== PASSWORD ======================
_password_hasher = PasswordHash.recommended()


def hash_password(plain_password: str) -> str:
    """Băm mật khẩu bằng Argon2id (mặc định của pwdlib)."""
    return _password_hasher.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Kiểm tra mật khẩu có khớp với hash đã lưu hay không."""
    return _password_hasher.verify(
        password=plain_password,
        hash=hashed_password,
    )