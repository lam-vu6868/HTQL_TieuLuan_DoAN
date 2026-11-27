from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security as SecurityService
from app.models.account import Account, Lecturer, Student, Course, CourseSection, SectionStudent
from app.models.enums import Role, GradingMode
from app.seed import data


async def _get_or_create(db: AsyncSession, model, lookup: dict, extra: dict | None = None):
    obj = await db.scalar(select(model).filter_by(**lookup))
    if obj:
        return obj, False
    obj = model(**lookup, **(extra or {}))
    db.add(obj)
    await db.flush()          # ← await
    return obj, True


async def _account(db: AsyncSession, email: str, role: Role) -> Account:
    acc, _ = await _get_or_create(     # ← await
        db, Account, {"email": email},
        {"password_hash": SecurityService.hash_password(data.DEFAULT_PASSWORD), "role": role},
    )
    return acc


async def run_seed(db: AsyncSession) -> None:
    # 1. Admin
    await _account(db, data.ADMIN["email"], Role.MANAGER)

    # 2. Giảng viên
    lecturers = []
    for l in data.LECTURERS:
        acc = await _account(db, l["email"], Role.LECTURER)
        lec, _ = await _get_or_create(
            db, Lecturer, {"account_id": acc.id},
            {"lecturer_code": l["lecturer_code"], "full_name": l["full_name"]},
        )
        lecturers.append(lec)

    # 3. Sinh viên
    students = []
    for s in data.STUDENTS:
        acc = await _account(db, s["email"], Role.STUDENT)
        stu, _ = await _get_or_create(
            db, Student, {"account_id": acc.id},
            {"student_code": s["student_code"], "full_name": s["full_name"]},
        )
        students.append(stu)

    # 4. Môn + lớp
    course, _ = await _get_or_create(
        db, Course, {"course_code": data.COURSE["course_code"]},
        {"course_name": data.COURSE["course_name"]},
    )
    now = datetime.now(timezone.utc)
    sec = data.SECTION
    section, _ = await _get_or_create(
        db, CourseSection, {"section_code": sec["section_code"]},
        {
            "course_id": course.id,
            "lecturer_id": lecturers[0].id,
            "semester": sec["semester"],
            "academic_year": sec["academic_year"],
            "registration_start_at": now,
            "registration_deadline": now + timedelta(days=14),
            "submission_deadline": now + timedelta(days=60),
            "min_members": sec["min_members"],
            "max_members": sec["max_members"],
            "grading_mode": GradingMode.SHARED,
            "pass_threshold": sec["pass_threshold"],
        },
    )

    # 5. Ghi danh
    for stu in students:
        await _get_or_create(
            db, SectionStudent,
            {"section_id": section.id, "student_id": stu.id},
        )

    await db.commit()