from enum import Enum


class Role(str, Enum):
    MANAGER = "MANAGER"
    LECTURER = "LECTURER"
    STUDENT = "STUDENT"


class GradingMode(str, Enum):
    SHARED = "SHARED"          # chấm chung: cả nhóm cùng một điểm
    INDIVIDUAL = "INDIVIDUAL"  # chấm riêng: mỗi sinh viên một điểm


class RegistrationType(str, Enum):
    ESSAY = "ESSAY"      # Tiểu luận
    PROJECT = "PROJECT"  # Đồ án


class Status(str, Enum):
    DRAFT = "DRAFT"
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class PublishStatus(str, Enum):
    UNPUBLISHED = "UNPUBLISHED"
    PUBLISHED = "PUBLISHED"