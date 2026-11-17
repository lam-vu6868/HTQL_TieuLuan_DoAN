"""Kiểm tra truy vấn ORM trên PostgreSQL, không giữ lại dữ liệu thử."""

import asyncio
import unittest
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from app.config import get_settings
from app.models.account import GiangVien, SinhVien, TaiKhoan
from app.models.academic import LopHocPhan, MonHoc, SinhVienLop
from app.models.assessment import BaiNop, KetQua, MocNop
from app.models.registration import HoSoDangKy, NhomTieuLuan, ThanhVienNhom
from app.models.term import DotDoAn, PhanCongHuongDan
from app.repositories import academic, registration, results, submissions


class RepositoryTests(unittest.TestCase):
    def test_repository_flow(self):
        asyncio.run(self._test_repository_flow(), loop_factory=asyncio.SelectorEventLoop)

    async def _test_repository_flow(self):
        engine = create_async_engine(get_settings().database_url, poolclass=NullPool)
        now = datetime.now(timezone.utc)
        token = uuid4().hex
        async with engine.connect() as connection:
            transaction = await connection.begin()
            session = AsyncSession(bind=connection, expire_on_commit=False)
            try:
                accounts = [
                    TaiKhoan(ten_dang_nhap=f"{token}-{i}@example.test", mat_khau_bam="hash", vai_tro=role)
                    for i, role in enumerate(("GIANG_VIEN", "SINH_VIEN", "SINH_VIEN"))
                ]
                for account in accounts:
                    await academic.save_account(session, account)
                teacher = GiangVien(tai_khoan_id=accounts[0].id, ma_giang_vien=f"GV-{token}", ho_ten="Giảng viên")
                students = [
                    SinhVien(tai_khoan_id=accounts[i].id, ma_sinh_vien=f"SV-{token}-{i}", ho_ten=f"Sinh viên {i}")
                    for i in (1, 2)
                ]
                await academic.save_teacher(session, teacher)
                for student in students:
                    await academic.save_student(session, student)
                course = MonHoc(ma_mon=f"MON-{token}", ten_mon="Tiểu luận")
                await academic.save_course(session, course)
                class_ = LopHocPhan(
                    mon_hoc_id=course.id, giang_vien_id=teacher.id, ma_lop=f"LOP-{token}",
                    hoc_ky=1, nam_hoc="2026-2027", so_thanh_vien_toi_thieu=1,
                    so_thanh_vien_toi_da=4, che_do_cham="RIENG", han_nop=now + timedelta(days=7),
                )
                term = DotDoAn(
                    ma_dot=f"DOT-{token}", ten_dot="Đồ án", hoc_ky=1, nam_hoc="2026-2027",
                    bat_dau_dang_ky=now - timedelta(days=1), han_dang_ky=now + timedelta(days=1),
                )
                await academic.save_class(session, class_)
                await academic.save_term(session, term)
                for student in students:
                    await academic.enroll_student(session, SinhVienLop(lop_id=class_.id, sinh_vien_id=student.id))

                self.assertEqual((await academic.get_account_by_email(session, accounts[1].ten_dang_nhap)).id, accounts[1].id)
                self.assertIsNotNone(await academic.get_student_class(session, students[0].id, class_.id))
                self.assertEqual((await academic.get_class_teacher(session, class_.id)).id, teacher.id)
                self.assertEqual([item.id for item in await academic.list_student_classes(session, students[0].id)], [class_.id])
                self.assertEqual([item.id for item in await academic.list_teacher_classes(session, teacher.id)], [class_.id])
                self.assertIn(term.id, [item.id for item in await academic.list_open_thesis_terms(session, now)])

                assignment = PhanCongHuongDan(dot_id=term.id, sinh_vien_id=students[0].id, giang_vien_id=teacher.id)
                await registration.save_supervisor_assignment(session, assignment)
                self.assertEqual((await academic.get_supervisor_assignment(session, term.id, students[0].id)).id, assignment.id)
                milestone = MocNop(phan_cong_id=assignment.id, ten_moc="Báo cáo cuối", thu_tu=1,
                                   han_nop=now + timedelta(days=5), la_moc_cuoi=True)
                await submissions.save_milestone(session, milestone)
                self.assertEqual((await submissions.get_milestone(session, milestone.id)).id, milestone.id)

                group = NhomTieuLuan(lop_id=class_.id, ten_nhom="Nhóm thử")
                await registration.save_group(session, group)
                for index, student in enumerate(students):
                    await registration.save_group_member(session, ThanhVienNhom(
                        nhom_id=group.id, lop_id=class_.id, sinh_vien_id=student.id, la_truong_nhom=index == 0,
                    ))
                self.assertEqual((await registration.get_group(session, group.id)).id, group.id)
                self.assertEqual(len(await registration.list_group_members(session, group.id)), 2)

                record = HoSoDangKy(
                    loai="TIEU_LUAN", ten_de_tai="Đề tài thử", mo_ta="Mô tả", sinh_vien_gui_id=students[0].id,
                    lop_id=class_.id, nhom_id=group.id, trang_thai="DA_DUYET",
                )
                await registration.save_registration(session, record)
                self.assertEqual((await registration.get_registration(session, record.id)).id, record.id)
                self.assertEqual(len(await registration.list_registered_topics(session, class_.id)), 1)
                self.assertEqual((await registration.find_active_registration(
                    session, loai="TIEU_LUAN", scope_id=class_.id, group_id=group.id,
                )).id, record.id)
                self.assertIsNone(await registration.find_active_registration(
                    session, loai="TIEU_LUAN", scope_id=class_.id, student_id=students[1].id,
                ))

                self.assertEqual(await submissions.get_class_deadline(session, class_.id), class_.han_nop)
                first = BaiNop(
                    ho_so_id=record.id, nguoi_nop_id=students[0].id, duong_dan_tep="first.pdf",
                    ten_tep_goc="first.pdf", nop_luc=now, nop_tre=False,
                )
                await submissions.upsert_submission(session, first)
                first.nhan_xet = "Nhận xét file cũ"
                await session.flush()
                replacement = BaiNop(
                    ho_so_id=record.id, nguoi_nop_id=students[0].id, duong_dan_tep="second.pdf",
                    ten_tep_goc="second.pdf", nop_luc=now + timedelta(minutes=1), nop_tre=True,
                )
                current = await submissions.upsert_submission(session, replacement)
                self.assertEqual(current.id, first.id)
                self.assertEqual((await submissions.get_current_submission(session, record.id)).duong_dan_tep, "second.pdf")
                self.assertTrue(current.nop_tre)
                self.assertIsNone(current.nhan_xet)

                self.assertEqual(await results.list_pending_publication(session), [])
                self.assertEqual(await results.get_statistics(session, loai="TIEU_LUAN", scope_id=class_.id),
                                 {"dat": 0, "khong_dat": 0, "chua_cham": 2})

                scores = [
                    KetQua(ho_so_id=record.id, sinh_vien_id=student.id, diem=score, nguoi_nhap_id=teacher.id,
                           nhap_luc=now, trang_thai_cong_bo="CHO_CONG_BO")
                    for student, score in zip(students, (8, 3))
                ]
                await results.save_student_scores(session, scores[:1])
                self.assertEqual(await results.list_pending_publication(session), [])
                self.assertEqual(await results.get_statistics(session, loai="TIEU_LUAN", scope_id=class_.id),
                                 {"dat": 1, "khong_dat": 0, "chua_cham": 1})
                await results.save_student_scores(session, scores[1:])
                self.assertEqual((await results.get_result(session, record.id, students[0].id)).diem, 8)
                self.assertEqual([item.id for item in await results.list_pending_publication(session)], [record.id])
                self.assertEqual(await results.get_statistics(session, loai="TIEU_LUAN", scope_id=class_.id),
                                 {"dat": 1, "khong_dat": 1, "chua_cham": 0})
                self.assertEqual(await results.list_student_published_results(session, students[0].id), [])
                for score in scores:
                    score.trang_thai_cong_bo = "DA_CONG_BO"
                await session.flush()
                self.assertEqual(len(await results.list_student_published_results(session, students[0].id)), 1)
                self.assertEqual(await results.list_pending_publication(session), [])

                thesis = HoSoDangKy(
                    loai="DO_AN", ten_de_tai="Đồ án thử", mo_ta="Mô tả", sinh_vien_gui_id=students[0].id,
                    dot_id=term.id, giang_vien_de_xuat_id=teacher.id, phan_cong_id=assignment.id,
                    trang_thai="DA_DUYET",
                )
                await registration.save_registration(session, thesis)
                self.assertEqual(await results.get_statistics(session, loai="DO_AN", scope_id=term.id),
                                 {"dat": 0, "khong_dat": 0, "chua_cham": 1})
                await results.save_student_scores(session, [KetQua(
                    ho_so_id=thesis.id, sinh_vien_id=students[0].id, diem=4, nguoi_nhap_id=teacher.id,
                    nhap_luc=now, trang_thai_cong_bo="CHO_CONG_BO",
                )])
                self.assertEqual(await results.get_statistics(session, loai="DO_AN", scope_id=term.id),
                                 {"dat": 1, "khong_dat": 0, "chua_cham": 0})
            finally:
                await session.close()
                await transaction.rollback()
        await engine.dispose()
