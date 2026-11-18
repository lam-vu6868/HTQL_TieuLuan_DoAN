"""Đợt Đồ án và phân công giảng viên hướng dẫn."""

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import mapped_column

from app.database import Base


class DotDoAn(Base):
    __tablename__ = "dot_do_an"

    id = mapped_column(BigInteger, primary_key=True)
    ma_dot = mapped_column(Text, unique=True, nullable=False)
    ten_dot = mapped_column(Text, nullable=False)
    hoc_ky = mapped_column(Integer, nullable=False)
    nam_hoc = mapped_column(Text, nullable=False)
    bat_dau_dang_ky = mapped_column(DateTime(timezone=True), nullable=False)
    han_dang_ky = mapped_column(DateTime(timezone=True), nullable=False)


class PhanCongHuongDan(Base):
    __tablename__ = "phan_cong_huong_dan"
    __table_args__ = (UniqueConstraint("dot_id", "sinh_vien_id"),)

    id = mapped_column(BigInteger, primary_key=True)
    dot_id = mapped_column(ForeignKey("dot_do_an.id"), nullable=False)
    sinh_vien_id = mapped_column(ForeignKey("sinh_vien.id"), nullable=False)
    giang_vien_id = mapped_column(ForeignKey("giang_vien.id"), nullable=False)
