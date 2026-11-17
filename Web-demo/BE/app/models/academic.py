"""Môn học, lớp học phần và danh sách sinh viên."""

from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, Integer, Numeric, Text, text
from sqlalchemy.orm import mapped_column

from app.database import Base


class MonHoc(Base):
    __tablename__ = "mon_hoc"

    id = mapped_column(BigInteger, primary_key=True)
    ma_mon = mapped_column(Text, unique=True, nullable=False)
    ten_mon = mapped_column(Text, nullable=False)


class LopHocPhan(Base):
    __tablename__ = "lop_hoc_phan"
    __table_args__ = (
        CheckConstraint("so_thanh_vien_toi_thieu >= 1 AND so_thanh_vien_toi_da >= so_thanh_vien_toi_thieu"),
        CheckConstraint("che_do_cham IN ('CHUNG', 'RIENG')"),
        CheckConstraint("nguong_dat BETWEEN 0 AND 10"),
    )

    id = mapped_column(BigInteger, primary_key=True)
    mon_hoc_id = mapped_column(ForeignKey("mon_hoc.id"), nullable=False)
    giang_vien_id = mapped_column(ForeignKey("giang_vien.id"), nullable=False)
    ma_lop = mapped_column(Text, nullable=False)
    hoc_ky = mapped_column(Integer, nullable=False)
    nam_hoc = mapped_column(Text, nullable=False)
    bat_dau_dang_ky = mapped_column(DateTime(timezone=True))
    han_dang_ky = mapped_column(DateTime(timezone=True))
    han_nop = mapped_column(DateTime(timezone=True))
    so_thanh_vien_toi_thieu = mapped_column(Integer, nullable=False)
    so_thanh_vien_toi_da = mapped_column(Integer, nullable=False)
    che_do_cham = mapped_column(Text, nullable=False)
    nguong_dat = mapped_column(Numeric(4, 2), nullable=False, server_default=text("4.0"))


class SinhVienLop(Base):
    __tablename__ = "sinh_vien_lop"

    lop_id = mapped_column(ForeignKey("lop_hoc_phan.id"), primary_key=True)
    sinh_vien_id = mapped_column(ForeignKey("sinh_vien.id"), primary_key=True)
