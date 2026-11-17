"""Điểm và thống kê theo từng sinh viên trong hồ sơ đã duyệt."""

from collections.abc import Sequence

from sqlalchemy import and_, case, func, select, union_all
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.academic import LopHocPhan
from app.models.assessment import KetQua
from app.models.registration import HoSoDangKy, ThanhVienNhom


def _participants():
    """Mỗi hồ sơ đã duyệt có một dòng cho từng sinh viên được chấm."""
    return union_all(
        select(HoSoDangKy.id.label("record_id"), HoSoDangKy.sinh_vien_gui_id.label("student_id"))
        .where(HoSoDangKy.trang_thai == "DA_DUYET", HoSoDangKy.nhom_id.is_(None)),
        select(HoSoDangKy.id.label("record_id"), ThanhVienNhom.sinh_vien_id.label("student_id"))
        .join(ThanhVienNhom, ThanhVienNhom.nhom_id == HoSoDangKy.nhom_id)
        .where(HoSoDangKy.trang_thai == "DA_DUYET"),
    ).subquery()


async def get_result(session: AsyncSession, registration_id: int, student_id: int) -> KetQua | None:
    """Lấy điểm của đúng một sinh viên trong một hồ sơ."""
    return await session.get(KetQua, (registration_id, student_id))


async def save_student_scores(session: AsyncSession, scores: Sequence[KetQua]) -> list[KetQua]:
    """Lưu một điểm mỗi sinh viên; điểm chung truyền nhiều dòng cùng giá trị."""
    saved = []
    for score in scores:
        current = await get_result(session, score.ho_so_id, score.sinh_vien_id)
        if current is None:
            session.add(score)
            current = score
        elif current is not score:
            current.diem = score.diem
            current.nguoi_nhap_id = score.nguoi_nhap_id
            current.nhap_luc = score.nhap_luc
            current.trang_thai_cong_bo = score.trang_thai_cong_bo
            current.nguoi_cong_bo_id = score.nguoi_cong_bo_id
            current.cong_bo_luc = score.cong_bo_luc
        saved.append(current)
    await session.flush()
    return saved


async def list_pending_publication(session: AsyncSession) -> list[HoSoDangKy]:
    """Lấy hồ sơ đã đủ điểm cho mọi thành viên nhưng chưa công bố hết."""
    participants = _participants()
    statement = (
        select(HoSoDangKy)
        .join(participants, participants.c.record_id == HoSoDangKy.id)
        .outerjoin(KetQua, and_(KetQua.ho_so_id == participants.c.record_id,
                                 KetQua.sinh_vien_id == participants.c.student_id))
        .group_by(HoSoDangKy.id)
        .having(func.count(KetQua.sinh_vien_id) == func.count(participants.c.student_id))
        .having(func.count(KetQua.sinh_vien_id).filter(
            KetQua.trang_thai_cong_bo != "DA_CONG_BO") > 0)
        .order_by(HoSoDangKy.id)
    )
    return list((await session.scalars(statement)).all())


async def list_student_published_results(session: AsyncSession, student_id: int) -> list[KetQua]:
    """Chỉ trả các dòng điểm đã công bố của chính sinh viên được hỏi."""
    return list((await session.scalars(
        select(KetQua).join(HoSoDangKy, HoSoDangKy.id == KetQua.ho_so_id)
        .where(KetQua.sinh_vien_id == student_id, KetQua.trang_thai_cong_bo == "DA_CONG_BO",
               HoSoDangKy.trang_thai == "DA_DUYET")
        .order_by(KetQua.ho_so_id)
    )).all())


async def get_statistics(session: AsyncSession, *, loai: str, scope_id: int) -> dict[str, int]:
    """Đếm sinh viên đạt, không đạt, chưa chấm trong một lớp hoặc đợt.

    Tiểu luận dùng ngưỡng của lớp; Đồ án dùng ngưỡng hồ sơ, mặc định 4.
    """
    if loai not in ("TIEU_LUAN", "DO_AN"):
        raise ValueError("Loại hồ sơ không hợp lệ")
    participants = _participants()
    threshold = case(
        (HoSoDangKy.loai == "TIEU_LUAN", LopHocPhan.nguong_dat),
        else_=func.coalesce(HoSoDangKy.nguong_dat, 4),
    )
    statement = (
        select(
            func.count().filter(KetQua.diem >= threshold),
            func.count().filter(KetQua.diem < threshold),
            func.count().filter(KetQua.diem.is_(None)),
        )
        .select_from(participants)
        .join(HoSoDangKy, HoSoDangKy.id == participants.c.record_id)
        .outerjoin(LopHocPhan, LopHocPhan.id == HoSoDangKy.lop_id)
        .outerjoin(KetQua, and_(KetQua.ho_so_id == participants.c.record_id,
                                 KetQua.sinh_vien_id == participants.c.student_id))
        .where(HoSoDangKy.loai == loai,
               HoSoDangKy.lop_id == scope_id if loai == "TIEU_LUAN" else HoSoDangKy.dot_id == scope_id)
    )
    passed, failed, ungraded = (await session.execute(statement)).one()
    return {"dat": passed, "khong_dat": failed, "chua_cham": ungraded}
