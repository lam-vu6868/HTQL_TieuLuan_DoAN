# app/models/registration.py
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger, Boolean, DateTime, Enum, ForeignKey, ForeignKeyConstraint,
    Index, Integer, Numeric, Text, UniqueConstraint, text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.models.enums import RegistrationType, Status


class ProjectPeriod(Base):
    __tablename__ = "project_periods"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    period_code: Mapped[str] = mapped_column(Text, unique=True)
    period_name: Mapped[str] = mapped_column(Text)
    semester: Mapped[int] = mapped_column(Integer)
    academic_year: Mapped[str] = mapped_column(Text)
    registration_start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    registration_deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class SupervisorAssignment(Base):
    __tablename__ = "supervisor_assignments"
    __table_args__ = (
        UniqueConstraint("period_id", "student_id", name="uq_assignment_period_student"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    period_id: Mapped[int] = mapped_column(ForeignKey("project_periods.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    lecturer_id: Mapped[int] = mapped_column(ForeignKey("lecturers.id"), index=True)


class EssayGroup(Base):
    __tablename__ = "essay_groups"
    __table_args__ = (
        # Để group_members dùng FK ghép (group_id, section_id)
        UniqueConstraint("id", "section_id", name="uq_group_id_section"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    section_id: Mapped[int] = mapped_column(
        ForeignKey("course_sections.id"), index=True
    )
    group_name: Mapped[str] = mapped_column(Text)


class GroupMember(Base):
    __tablename__ = "group_members"
    __table_args__ = (
        # Nhóm phải thuộc đúng lớp này
        ForeignKeyConstraint(
            ["group_id", "section_id"],
            ["essay_groups.id", "essay_groups.section_id"],
        ),
        # Sinh viên phải thuộc đúng lớp này
        ForeignKeyConstraint(
            ["section_id", "student_id"],
            ["section_students.section_id", "section_students.student_id"],
        ),
        # Một sinh viên chỉ ở một nhóm trong một lớp
        UniqueConstraint("section_id", "student_id", name="uq_member_section_student"),
        # Mỗi nhóm tối đa một trưởng nhóm
        Index(
            "uq_group_one_leader",
            "group_id",
            unique=True,
            postgresql_where=text("is_leader"),
        ),
    )

    group_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    student_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    section_id: Mapped[int] = mapped_column(BigInteger)
    is_leader: Mapped[bool] = mapped_column(Boolean, default=False)


class TopicRegistration(Base):
    __tablename__ = "topic_registrations"
    __table_args__ = (
        # Mỗi nhóm chỉ một hồ sơ đang xử lý
        Index(
            "uq_active_group",
            "group_id",
            unique=True,
            postgresql_where=text("group_id IS NOT NULL AND status IN ('PENDING','APPROVED')"),
        ),
        # Tiểu luận cá nhân: mỗi sinh viên một hồ sơ đang xử lý trong lớp
        Index(
            "uq_active_essay_personal",
            "section_id", "submitter_id",
            unique=True,
            postgresql_where=text(
                "section_id IS NOT NULL AND group_id IS NULL AND status IN ('PENDING','APPROVED')"
            ),
        ),
        # Đồ án: mỗi sinh viên một hồ sơ đang xử lý trong đợt
        Index(
            "uq_active_project",
            "period_id", "submitter_id",
            unique=True,
            postgresql_where=text(
                "period_id IS NOT NULL AND status IN ('PENDING','APPROVED')"
            ),
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    registration_type: Mapped[RegistrationType] = mapped_column(
        Enum(RegistrationType, native_enum=False)
    )
    topic_title: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    submitter_id: Mapped[int] = mapped_column(ForeignKey("students.id"), index=True)
    status: Mapped[Status] = mapped_column(
        Enum(Status, native_enum=False), default=Status.DRAFT
    )

    section_id: Mapped[int | None] = mapped_column(ForeignKey("course_sections.id"))
    period_id: Mapped[int | None] = mapped_column(ForeignKey("project_periods.id"))
    group_id: Mapped[int | None] = mapped_column(ForeignKey("essay_groups.id"))
    proposed_lecturer_id: Mapped[int | None] = mapped_column(ForeignKey("lecturers.id"))
    assignment_id: Mapped[int | None] = mapped_column(
        ForeignKey("supervisor_assignments.id")
    )
    pass_threshold: Mapped[Decimal | None] = mapped_column(Numeric(4, 2))

    submit_count: Mapped[int] = mapped_column(Integer, default=0)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    reviewer_id: Mapped[int | None] = mapped_column(ForeignKey("lecturers.id"))
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    rejection_reason: Mapped[str | None] = mapped_column(Text)