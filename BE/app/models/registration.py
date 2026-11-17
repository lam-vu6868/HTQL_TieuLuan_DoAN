"""Nhóm Tiểu luận và hồ sơ đăng ký đề tài."""

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    Numeric,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import mapped_column

from app.database import Base


class NhomTieuLuan(Base):
    __tablename__ = "nhom_tieu_luan"
    __table_args__ = (UniqueConstraint("id", "lop_id"),)

    id = mapped_column(BigInteger, primary_key=True)
    lop_id = mapped_column(ForeignKey("lop_hoc_phan.id"), nullable=False)
    ten_nhom = mapped_column(Text, nullable=False)


class ThanhVienNhom(Base):
    __tablename__ = "thanh_vien_nhom"
    __table_args__ = (
        ForeignKeyConstraint(["nhom_id", "lop_id"], ["nhom_tieu_luan.id", "nhom_tieu_luan.lop_id"]),
        ForeignKeyConstraint(["lop_id", "sinh_vien_id"], ["sinh_vien_lop.lop_id", "sinh_vien_lop.sinh_vien_id"]),
        UniqueConstraint("lop_id", "sinh_vien_id"),
        Index("uq_truong_nhom", "nhom_id", unique=True, postgresql_where=text("la_truong_nhom")),
    )

    nhom_id = mapped_column(BigInteger, primary_key=True)
    sinh_vien_id = mapped_column(BigInteger, primary_key=True)
    lop_id = mapped_column(BigInteger, nullable=False)
    la_truong_nhom = mapped_column(Boolean, nullable=False, server_default=text("false"))


class HoSoDangKy(Base):
    __tablename__ = "ho_so_dang_ky"
    __table_args__ = (
        ForeignKeyConstraint(["nhom_id", "lop_id"], ["nhom_tieu_luan.id", "nhom_tieu_luan.lop_id"]),
        CheckConstraint("loai IN ('TIEU_LUAN', 'DO_AN')"),
        CheckConstraint("trang_thai IN ('NHAP', 'CHO_DUYET', 'DA_DUYET', 'TU_CHOI')"),
        CheckConstraint("trang_thai = 'NHAP' OR (loai = 'TIEU_LUAN' AND lop_id IS NOT NULL AND dot_id IS NULL) OR (loai = 'DO_AN' AND dot_id IS NOT NULL AND lop_id IS NULL AND giang_vien_de_xuat_id IS NOT NULL)"),
        CheckConstraint("nguong_dat IS NULL OR nguong_dat BETWEEN 0 AND 10"),
        CheckConstraint("lan_gui >= 0"),
        Index(
            "uq_ho_so_tieu_luan_ca_nhan_dang_xu_ly", "lop_id", "sinh_vien_gui_id", unique=True,
            postgresql_where=text("loai = 'TIEU_LUAN' AND nhom_id IS NULL AND trang_thai IN ('CHO_DUYET', 'DA_DUYET')"),
        ),
        Index(
            "uq_ho_so_tieu_luan_nhom_dang_xu_ly", "lop_id", "nhom_id", unique=True,
            postgresql_where=text("loai = 'TIEU_LUAN' AND nhom_id IS NOT NULL AND trang_thai IN ('CHO_DUYET', 'DA_DUYET')"),
        ),
        Index(
            "uq_ho_so_do_an_dang_xu_ly", "dot_id", "sinh_vien_gui_id", unique=True,
            postgresql_where=text("loai = 'DO_AN' AND trang_thai IN ('CHO_DUYET', 'DA_DUYET')"),
        ),
    )

    id = mapped_column(BigInteger, primary_key=True)
    loai = mapped_column(Text, nullable=False)
    ten_de_tai = mapped_column(Text, nullable=False)
    mo_ta = mapped_column(Text, nullable=False)
    sinh_vien_gui_id = mapped_column(ForeignKey("sinh_vien.id"), nullable=False)
    trang_thai = mapped_column(Text, nullable=False, server_default=text("'NHAP'"))
    lop_id = mapped_column(ForeignKey("lop_hoc_phan.id"))
    dot_id = mapped_column(ForeignKey("dot_do_an.id"))
    nhom_id = mapped_column(BigInteger)
    giang_vien_de_xuat_id = mapped_column(ForeignKey("giang_vien.id"))
    phan_cong_id = mapped_column(ForeignKey("phan_cong_huong_dan.id"))
    nguong_dat = mapped_column(Numeric(4, 2))
    lan_gui = mapped_column(Integer, nullable=False, server_default=text("0"))
    gui_luc = mapped_column(DateTime(timezone=True))
    nguoi_duyet_id = mapped_column(ForeignKey("giang_vien.id"))
    duyet_luc = mapped_column(DateTime(timezone=True))
    ly_do_tu_choi = mapped_column(Text)
