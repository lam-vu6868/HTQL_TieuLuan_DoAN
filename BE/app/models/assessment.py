"""Mốc nộp, bài nộp và kết quả từng sinh viên."""

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import mapped_column

from app.database import Base


class MocNop(Base):
    __tablename__ = "moc_nop"
    __table_args__ = (
        UniqueConstraint("phan_cong_id", "thu_tu"),
        Index("uq_moc_cuoi", "phan_cong_id", unique=True, postgresql_where=text("la_moc_cuoi")),
    )

    id = mapped_column(BigInteger, primary_key=True)
    phan_cong_id = mapped_column(ForeignKey("phan_cong_huong_dan.id"), nullable=False)
    ten_moc = mapped_column(Text, nullable=False)
    thu_tu = mapped_column(Integer, nullable=False)
    han_nop = mapped_column(DateTime(timezone=True), nullable=False)
    la_moc_cuoi = mapped_column(Boolean, nullable=False, server_default=text("false"))


class BaiNop(Base):
    __tablename__ = "bai_nop"
    __table_args__ = (
        UniqueConstraint("ho_so_id", "moc_nop_id"),
        Index("uq_bai_nop_tieu_luan", "ho_so_id", unique=True, postgresql_where=text("moc_nop_id IS NULL")),
    )

    id = mapped_column(BigInteger, primary_key=True)
    ho_so_id = mapped_column(ForeignKey("ho_so_dang_ky.id"), nullable=False)
    moc_nop_id = mapped_column(ForeignKey("moc_nop.id"))
    nguoi_nop_id = mapped_column(ForeignKey("sinh_vien.id"), nullable=False)
    duong_dan_tep = mapped_column(Text, nullable=False)
    ten_tep_goc = mapped_column(Text, nullable=False)
    nop_luc = mapped_column(DateTime(timezone=True), nullable=False)
    nop_tre = mapped_column(Boolean, nullable=False)
    nhan_xet = mapped_column(Text)
    nguoi_nhan_xet_id = mapped_column(ForeignKey("giang_vien.id"))
    nhan_xet_luc = mapped_column(DateTime(timezone=True))


class KetQua(Base):
    __tablename__ = "ket_qua"
    __table_args__ = (CheckConstraint("diem BETWEEN 0 AND 10"),)

    ho_so_id = mapped_column(ForeignKey("ho_so_dang_ky.id"), primary_key=True)
    sinh_vien_id = mapped_column(ForeignKey("sinh_vien.id"), primary_key=True)
    diem = mapped_column(Numeric(4, 2), nullable=False)
    nguoi_nhap_id = mapped_column(ForeignKey("giang_vien.id"), nullable=False)
    nhap_luc = mapped_column(DateTime(timezone=True), nullable=False)
    trang_thai_cong_bo = mapped_column(Text, nullable=False)
    nguoi_cong_bo_id = mapped_column(ForeignKey("tai_khoan.id"))
    cong_bo_luc = mapped_column(DateTime(timezone=True))
