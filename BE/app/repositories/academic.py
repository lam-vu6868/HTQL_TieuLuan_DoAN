"""Truy vấn tài khoản, lớp và đợt; các hàm lưu chỉ flush, không commit."""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import GiangVien, SinhVien, TaiKhoan
from app.models.academic import LopHocPhan, MonHoc, SinhVienLop
from app.models.term import DotDoAn, PhanCongHuongDan


async def get_account_by_email(session: AsyncSession, email: str) -> TaiKhoan | None:
    """Tìm tài khoản theo email đăng nhập; trả None nếu không có."""
    return await session.scalar(select(TaiKhoan).where(TaiKhoan.ten_dang_nhap == email))


async def get_student_class(session: AsyncSession, student_id: int, class_id: int) -> SinhVienLop | None:
    """Kiểm tra sinh viên có trong lớp bằng bản ghi xếp lớp."""
    return await session.get(SinhVienLop, (class_id, student_id))


async def get_class_teacher(session: AsyncSession, class_id: int) -> GiangVien | None:
    """Lấy giảng viên phụ trách lớp để service kiểm tra quyền duyệt."""
    return await session.scalar(
        select(GiangVien).join(LopHocPhan, LopHocPhan.giang_vien_id == GiangVien.id)
        .where(LopHocPhan.id == class_id)
    )


async def list_student_classes(session: AsyncSession, student_id: int) -> list[LopHocPhan]:
    """Liệt kê các lớp học phần đã xếp cho một sinh viên."""
    return list((await session.scalars(
        select(LopHocPhan).join(SinhVienLop).where(SinhVienLop.sinh_vien_id == student_id)
        .order_by(LopHocPhan.id)
    )).all())


async def list_teacher_classes(session: AsyncSession, teacher_id: int) -> list[LopHocPhan]:
    """Liệt kê các lớp học phần do giảng viên phụ trách."""
    return list((await session.scalars(
        select(LopHocPhan).where(LopHocPhan.giang_vien_id == teacher_id).order_by(LopHocPhan.id)
    )).all())


async def list_open_thesis_terms(session: AsyncSession, now: datetime) -> list[DotDoAn]:
    """Lấy các đợt Đồ án còn trong khoảng thời gian đăng ký tại `now`."""
    return list((await session.scalars(
        select(DotDoAn).where(DotDoAn.bat_dau_dang_ky <= now, DotDoAn.han_dang_ky >= now)
        .order_by(DotDoAn.han_dang_ky)
    )).all())


async def get_supervisor_assignment(
    session: AsyncSession, term_id: int, student_id: int,
) -> PhanCongHuongDan | None:
    """Tìm GVHD chính thức của sinh viên trong một đợt Đồ án."""
    return await session.scalar(select(PhanCongHuongDan).where(
        PhanCongHuongDan.dot_id == term_id, PhanCongHuongDan.sinh_vien_id == student_id,
    ))


async def save_account(session: AsyncSession, account: TaiKhoan) -> TaiKhoan:
    """Lưu tài khoản để lấy ID và kiểm tra ràng buộc CSDL trong giao dịch."""
    session.add(account)
    await session.flush()
    return account


async def save_student(session: AsyncSession, student: SinhVien) -> SinhVien:
    """Lưu hồ sơ sinh viên gắn với tài khoản đã tạo."""
    session.add(student)
    await session.flush()
    return student


async def save_teacher(session: AsyncSession, teacher: GiangVien) -> GiangVien:
    """Lưu hồ sơ giảng viên gắn với tài khoản đã tạo."""
    session.add(teacher)
    await session.flush()
    return teacher


async def save_course(session: AsyncSession, course: MonHoc) -> MonHoc:
    """Lưu môn học để lớp học phần tham chiếu tới."""
    session.add(course)
    await session.flush()
    return course


async def save_class(session: AsyncSession, class_: LopHocPhan) -> LopHocPhan:
    """Lưu lớp học phần cùng giảng viên, hạn nộp và chế độ chấm."""
    session.add(class_)
    await session.flush()
    return class_


async def save_term(session: AsyncSession, term: DotDoAn) -> DotDoAn:
    """Lưu đợt Đồ án và thời gian nhận đăng ký."""
    session.add(term)
    await session.flush()
    return term


async def enroll_student(session: AsyncSession, enrollment: SinhVienLop) -> SinhVienLop:
    """Ghi sinh viên vào lớp; khóa ghép ngăn xếp trùng cùng lớp."""
    session.add(enrollment)
    await session.flush()
    return enrollment
