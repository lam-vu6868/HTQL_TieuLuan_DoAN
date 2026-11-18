from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.academic import LopHocPhan, MonHoc, SinhVienLop
from app.models.account import GiangVien
from app.models.registration import HoSoDangKy


class ReportRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def slow_db(self, seconds: float) -> None:
        """Truy vấn chậm thật ở phía DB; await nên không chặn event loop."""
        await self.session.execute(select(func.pg_sleep(seconds)))

    async def class_summary(self):
        # Số sinh viên mỗi lớp
        sv = (
            select(SinhVienLop.lop_id, func.count().label("so_sv"))
            .group_by(SinhVienLop.lop_id)
            .subquery()
        )
        # Đếm hồ sơ tiểu luận theo trạng thái (COUNT ... FILTER của PostgreSQL)
        hs = (
            select(
                HoSoDangKy.lop_id,
                func.count().label("tong"),
                func.count().filter(HoSoDangKy.trang_thai == "CHO_DUYET").label("cho_duyet"),
                func.count().filter(HoSoDangKy.trang_thai == "DA_DUYET").label("da_duyet"),
                func.count().filter(HoSoDangKy.trang_thai == "TU_CHOI").label("tu_choi"),
            )
            .where(HoSoDangKy.loai == "TIEU_LUAN")
            .group_by(HoSoDangKy.lop_id)
            .subquery()
        )

        stmt = (
            select(
                LopHocPhan.id.label("lop_id"),
                LopHocPhan.ma_lop,
                MonHoc.ten_mon,
                GiangVien.ho_ten.label("giang_vien"),
                func.coalesce(sv.c.so_sv, 0).label("so_sinh_vien"),
                func.coalesce(hs.c.tong, 0).label("tong_ho_so"),
                func.coalesce(hs.c.cho_duyet, 0).label("cho_duyet"),
                func.coalesce(hs.c.da_duyet, 0).label("da_duyet"),
                func.coalesce(hs.c.tu_choi, 0).label("tu_choi"),
            )
            .join(MonHoc, MonHoc.id == LopHocPhan.mon_hoc_id)
            .join(GiangVien, GiangVien.id == LopHocPhan.giang_vien_id)
            .outerjoin(sv, sv.c.lop_id == LopHocPhan.id)
            .outerjoin(hs, hs.c.lop_id == LopHocPhan.id)
            .order_by(LopHocPhan.ma_lop)
        )
        result = await self.session.execute(stmt)
        return result.mappings().all()