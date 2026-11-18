"""Tài khoản, sinh viên và giảng viên."""

from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, Text
from sqlalchemy.orm import mapped_column

from app.database import Base


class TaiKhoan(Base):
    __tablename__ = "tai_khoan"
    __table_args__ = (
        CheckConstraint("vai_tro IN ('QUAN_LY', 'GIANG_VIEN', 'SINH_VIEN')"),
    )

    id = mapped_column(BigInteger, primary_key=True)
    ten_dang_nhap = mapped_column(Text, unique=True, nullable=False)
    mat_khau_bam = mapped_column(Text, nullable=False)
    vai_tro = mapped_column(Text, nullable=False)
    reset_token_hash = mapped_column(Text)
    reset_expires_at = mapped_column(DateTime(timezone=True))


class SinhVien(Base):
    __tablename__ = "sinh_vien"

    id = mapped_column(BigInteger, primary_key=True)
    tai_khoan_id = mapped_column(ForeignKey("tai_khoan.id"), unique=True, nullable=False)
    ma_sinh_vien = mapped_column(Text, unique=True, nullable=False)
    ho_ten = mapped_column(Text, nullable=False)


class GiangVien(Base):
    __tablename__ = "giang_vien"

    id = mapped_column(BigInteger, primary_key=True)
    tai_khoan_id = mapped_column(ForeignKey("tai_khoan.id"), unique=True, nullable=False)
    ma_giang_vien = mapped_column(Text, unique=True, nullable=False)
    ho_ten = mapped_column(Text, nullable=False)
