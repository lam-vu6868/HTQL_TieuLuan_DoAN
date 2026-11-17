"""Truy vấn nhóm và hồ sơ; service quyết định quyền, trạng thái và commit."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.registration import HoSoDangKy, NhomTieuLuan, ThanhVienNhom
from app.models.term import PhanCongHuongDan


async def list_registered_topics(session: AsyncSession, class_id: int) -> list[HoSoDangKy]:
    """Liệt kê đề tài Tiểu luận đang chờ hoặc đã duyệt trong lớp."""
    return list((await session.scalars(select(HoSoDangKy).where(
        HoSoDangKy.loai == "TIEU_LUAN", HoSoDangKy.lop_id == class_id,
        HoSoDangKy.trang_thai.in_(("CHO_DUYET", "DA_DUYET")),
    ).order_by(HoSoDangKy.id))).all())


async def get_group(session: AsyncSession, group_id: int, for_update: bool = False) -> NhomTieuLuan | None:
    """Lấy nhóm; `for_update` khóa dòng khi service sửa thành viên."""
    statement = select(NhomTieuLuan).where(NhomTieuLuan.id == group_id)
    return await session.scalar(statement.with_for_update() if for_update else statement)


async def get_registration(
    session: AsyncSession, registration_id: int, for_update: bool = False,
) -> HoSoDangKy | None:
    """Lấy hồ sơ; có thể khóa dòng trước khi duyệt hoặc đổi trạng thái."""
    statement = select(HoSoDangKy).where(HoSoDangKy.id == registration_id)
    return await session.scalar(statement.with_for_update() if for_update else statement)


async def find_active_registration(
    session: AsyncSession, *, loai: str, scope_id: int,
    student_id: int | None = None, group_id: int | None = None,
) -> HoSoDangKy | None:
    """Tìm hồ sơ chờ/đã duyệt trong lớp hoặc đợt của đúng cá nhân/nhóm.

    `scope_id` là mã lớp cho Tiểu luận, mã đợt cho Đồ án.
    """
    if loai not in ("TIEU_LUAN", "DO_AN") or (student_id is None) == (group_id is None):
        raise ValueError("Chọn đúng một sinh viên hoặc nhóm và loại hồ sơ hợp lệ")
    if loai == "DO_AN" and group_id is not None:
        raise ValueError("Hồ sơ Đồ án không thuộc nhóm")
    statement = select(HoSoDangKy).where(
        HoSoDangKy.loai == loai,
        HoSoDangKy.trang_thai.in_(("CHO_DUYET", "DA_DUYET")),
        HoSoDangKy.dot_id == scope_id if loai == "DO_AN" else HoSoDangKy.lop_id == scope_id,
        HoSoDangKy.nhom_id == group_id if group_id is not None else HoSoDangKy.sinh_vien_gui_id == student_id,
    )
    if group_id is None and loai == "TIEU_LUAN":
        statement = statement.where(HoSoDangKy.nhom_id.is_(None))
    return await session.scalar(statement)


async def list_group_members(session: AsyncSession, group_id: int) -> list[ThanhVienNhom]:
    """Liệt kê thành viên của nhóm để kiểm tra sĩ số và người được chấm."""
    return list((await session.scalars(select(ThanhVienNhom).where(
        ThanhVienNhom.nhom_id == group_id,
    ).order_by(ThanhVienNhom.sinh_vien_id))).all())


async def save_group(session: AsyncSession, group: NhomTieuLuan) -> NhomTieuLuan:
    """Lưu nhóm Tiểu luận và cấp ID trước khi thêm thành viên."""
    session.add(group)
    await session.flush()
    return group


async def save_group_member(session: AsyncSession, member: ThanhVienNhom) -> ThanhVienNhom:
    """Lưu thành viên nhóm; FK CSDL buộc sinh viên thuộc đúng lớp."""
    session.add(member)
    await session.flush()
    return member


async def save_registration(session: AsyncSession, record: HoSoDangKy) -> HoSoDangKy:
    """Lưu hồ sơ đề tài; service tự kiểm tra hạn, quyền và chuyển trạng thái."""
    session.add(record)
    await session.flush()
    return record


async def save_supervisor_assignment(
    session: AsyncSession, assignment: PhanCongHuongDan,
) -> PhanCongHuongDan:
    """Lưu GVHD khi Đồ án được duyệt trong cùng giao dịch với hồ sơ."""
    session.add(assignment)
    await session.flush()
    return assignment
