"""Truy vấn mốc nộp và metadata; file thật được service quản lý."""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.academic import LopHocPhan
from app.models.assessment import BaiNop, MocNop
from app.models.registration import HoSoDangKy


async def get_milestone(session: AsyncSession, milestone_id: int) -> MocNop | None:
    """Lấy một mốc nộp Đồ án theo ID."""
    return await session.get(MocNop, milestone_id)


async def save_milestone(session: AsyncSession, milestone: MocNop) -> MocNop:
    """Lưu mốc do GVHD đặt; quyền GVHD được service kiểm tra."""
    session.add(milestone)
    await session.flush()
    return milestone


async def get_class_deadline(session: AsyncSession, class_id: int) -> datetime | None:
    """Lấy hạn nộp Tiểu luận của lớp để tính nộp trễ."""
    return await session.scalar(select(LopHocPhan.han_nop).where(LopHocPhan.id == class_id))


async def get_current_submission(
    session: AsyncSession, registration_id: int, milestone_id: int | None = None,
    for_update: bool = False,
) -> BaiNop | None:
    """Lấy file hiện hành của hồ sơ hoặc một mốc; có thể khóa khi thay file."""
    statement = select(BaiNop).where(BaiNop.ho_so_id == registration_id)
    statement = statement.where(
        BaiNop.moc_nop_id.is_(None) if milestone_id is None else BaiNop.moc_nop_id == milestone_id
    )
    return await session.scalar(statement.with_for_update() if for_update else statement)


async def upsert_submission(session: AsyncSession, submission: BaiNop) -> BaiNop:
    """Tạo hoặc thay metadata file hiện hành, giữ một dòng cho mỗi hồ sơ/mốc.

    Khóa hồ sơ để hai lần nộp đồng thời không cùng tạo một dòng; khi thay file,
    xóa nhận xét của file cũ. Service chỉ xóa file cũ sau khi giao dịch thành công.
    """
    await session.scalar(select(HoSoDangKy.id).where(HoSoDangKy.id == submission.ho_so_id).with_for_update())
    current = await get_current_submission(
        session, submission.ho_so_id, submission.moc_nop_id, for_update=True,
    )
    if current is None:
        session.add(submission)
        current = submission
    else:
        current.nguoi_nop_id = submission.nguoi_nop_id
        current.duong_dan_tep = submission.duong_dan_tep
        current.ten_tep_goc = submission.ten_tep_goc
        current.nop_luc = submission.nop_luc
        current.nop_tre = submission.nop_tre
        current.nhan_xet = None
        current.nguoi_nhan_xet_id = None
        current.nhan_xet_luc = None
    await session.flush()
    return current
