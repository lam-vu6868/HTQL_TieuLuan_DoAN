"""Seed dữ liệu demo cho báo cáo (≈1000 dòng ho_so_dang_ky).

Chạy từ thư mục BE:
    python seed.py            # seed nếu DB còn trống
    python seed.py --reset    # xóa dữ liệu cũ rồi seed lại
"""

import argparse
import asyncio
import random
import sys
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select, text

# Import đủ module để SQLAlchemy resolve hết khóa ngoại (dot_do_an, phan_cong_huong_dan...)
from app.models import academic, account, assessment, registration, term  # noqa: F401
from app.models.academic import LopHocPhan, MonHoc, SinhVienLop
from app.models.account import GiangVien, SinhVien, TaiKhoan
from app.models.registration import HoSoDangKy
from app.database import AsyncSessionLocal, engine

try:
    from app.core.security import hash_password
except ImportError:  # chưa có hàm này thì dùng chuỗi giả, demo không đăng nhập nên không sao
    def hash_password(_: str) -> str:
        return "seed-placeholder-hash"

NUM_STUDENTS = 200
NUM_LECTURERS = 3
NUM_CLASSES = 5          # 200 SV x 5 lớp = 1000 hồ sơ

HO = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ"]
DEM = ["Văn", "Thị", "Minh", "Quốc", "Ngọc", "Gia", "Thanh", "Hữu", "Anh", "Thùy"]
TEN = ["An", "Bình", "Châu", "Dũng", "Giang", "Hà", "Hiếu", "Khoa", "Lan", "Linh",
       "Minh", "Nam", "Phúc", "Quân", "Sơn", "Tâm", "Thảo", "Trang", "Tuấn", "Vy"]

DE_TAI = [
    "Hệ thống quản lý thư viện", "Ứng dụng đặt lịch khám bệnh", "Website bán hàng trực tuyến",
    "Quản lý nhân sự doanh nghiệp nhỏ", "Ứng dụng học từ vựng", "Hệ thống điểm danh bằng QR",
    "Quản lý kho hàng", "Ứng dụng chia sẻ chuyến đi", "Hệ thống quản lý ký túc xá",
    "Ứng dụng theo dõi chi tiêu cá nhân", "Chatbot hỗ trợ tuyển sinh", "Quản lý phòng gym",
]

STATUSES = ["NHAP", "CHO_DUYET", "DA_DUYET", "TU_CHOI"]
WEIGHTS = [10, 25, 45, 20]


def make_name() -> str:
    return f"{random.choice(HO)} {random.choice(DEM)} {random.choice(TEN)}"


async def reset_data(session) -> None:
    await session.execute(text(
        "TRUNCATE TABLE ho_so_dang_ky, sinh_vien_lop, lop_hoc_phan, mon_hoc, "
        "sinh_vien, giang_vien, tai_khoan RESTART IDENTITY CASCADE"
    ))
    await session.commit()
    print("Đã xóa dữ liệu cũ.")


async def seed(session) -> None:
    random.seed(42)  # cùng kết quả mỗi lần seed
    pw = hash_password("123456")  # hash một lần, dùng chung
    now = datetime.now(timezone.utc)

    # 1. Tài khoản
    accounts = [TaiKhoan(ten_dang_nhap="admin", mat_khau_bam=pw, vai_tro="QUAN_LY")]
    accounts += [TaiKhoan(ten_dang_nhap=f"gv{i:02d}", mat_khau_bam=pw, vai_tro="GIANG_VIEN")
                 for i in range(1, NUM_LECTURERS + 1)]
    accounts += [TaiKhoan(ten_dang_nhap=f"sv{i:04d}", mat_khau_bam=pw, vai_tro="SINH_VIEN")
                 for i in range(1, NUM_STUDENTS + 1)]
    session.add_all(accounts)
    await session.flush()

    gv_acc = [a for a in accounts if a.vai_tro == "GIANG_VIEN"]
    sv_acc = [a for a in accounts if a.vai_tro == "SINH_VIEN"]

    # 2. Giảng viên, sinh viên
    lecturers = [GiangVien(tai_khoan_id=a.id, ma_giang_vien=f"GV{i:03d}", ho_ten=make_name())
                 for i, a in enumerate(gv_acc, start=1)]
    students = [SinhVien(tai_khoan_id=a.id, ma_sinh_vien=f"22DH{i:04d}", ho_ten=make_name())
                for i, a in enumerate(sv_acc, start=1)]
    session.add_all(lecturers + students)

    # 3. Môn học
    subjects = [MonHoc(ma_mon="OOP101", ten_mon="Ứng dụng hướng đối tượng"),
                MonHoc(ma_mon="WEB201", ten_mon="Lập trình Web")]
    session.add_all(subjects)
    await session.flush()

    # 4. Lớp học phần (5 lớp, chia đều cho các giảng viên và 2 môn)
    classes = []
    for i in range(NUM_CLASSES):
        classes.append(LopHocPhan(
            mon_hoc_id=subjects[i % len(subjects)].id,
            giang_vien_id=lecturers[i % len(lecturers)].id,
            ma_lop=f"LHP{i + 1:02d}",
            hoc_ky=1,
            nam_hoc="2026-2027",
            bat_dau_dang_ky=now - timedelta(days=30),
            han_dang_ky=now + timedelta(days=30),
            han_nop=now + timedelta(days=90),
            so_thanh_vien_toi_thieu=1,
            so_thanh_vien_toi_da=3,
            che_do_cham="CHUNG",
        ))
    session.add_all(classes)
    await session.flush()

    # 5. Sinh viên - lớp (mọi SV học mọi lớp) và hồ sơ đăng ký cá nhân
    enrollments, registrations = [], []
    for lop in classes:
        for sv in students:
            enrollments.append(SinhVienLop(lop_id=lop.id, sinh_vien_id=sv.id))

            status = random.choices(STATUSES, weights=WEIGHTS)[0]
            hs = HoSoDangKy(
                loai="TIEU_LUAN",
                ten_de_tai=f"{random.choice(DE_TAI)} #{random.randint(1, 999)}",
                mo_ta="Mô tả demo: xây dựng hệ thống theo hướng đối tượng, có phân tích thiết kế UML.",
                sinh_vien_gui_id=sv.id,
                trang_thai=status,
                lop_id=lop.id,
                lan_gui=0,
            )
            if status != "NHAP":
                hs.gui_luc = now - timedelta(days=random.randint(1, 25))
                hs.lan_gui = 1
            if status in ("DA_DUYET", "TU_CHOI"):
                hs.nguoi_duyet_id = lop.giang_vien_id
                hs.duyet_luc = hs.gui_luc + timedelta(days=random.randint(1, 3))
            if status == "TU_CHOI":
                hs.lan_gui = random.randint(1, 2)
                hs.ly_do_tu_choi = "Đề tài chưa rõ phạm vi, vui lòng chỉnh sửa và gửi lại."
            registrations.append(hs)

    session.add_all(enrollments)
    session.add_all(registrations)
    await session.commit()


async def summarize(session) -> None:
    print("\n--- Kết quả seed ---")
    for model in (TaiKhoan, GiangVien, SinhVien, MonHoc, LopHocPhan, SinhVienLop, HoSoDangKy):
        n = (await session.execute(select(func.count()).select_from(model))).scalar_one()
        print(f"{model.__tablename__:<16} {n}")
    rows = (await session.execute(
        select(HoSoDangKy.trang_thai, func.count()).group_by(HoSoDangKy.trang_thai)
    )).all()
    print("\nho_so_dang_ky theo trạng thái:", {s: c for s, c in rows})


async def main(reset: bool) -> None:
    async with AsyncSessionLocal() as session:
        if reset:
            await reset_data(session)
        else:
            existing = (await session.execute(
                select(func.count()).select_from(HoSoDangKy))).scalar_one()
            if existing:
                print(f"DB đã có {existing} hồ sơ. Dùng --reset nếu muốn seed lại.")
                return
        await seed(session)
        await summarize(session)
    await engine.dispose()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Xóa dữ liệu cũ trước khi seed")
    asyncio.run(main(parser.parse_args().reset))
