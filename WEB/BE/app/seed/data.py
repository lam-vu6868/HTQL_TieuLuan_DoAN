DEFAULT_PASSWORD = "Password@123"  # chỉ dùng cho môi trường dev

ADMIN = {"email": "admin@bdu.edu.vn"}

LECTURERS = [
    {"email": "gv01@bdu.edu.vn", "lecturer_code": "GV001", "full_name": "Nguyễn Văn An"},
    {"email": "gv02@bdu.edu.vn", "lecturer_code": "GV002", "full_name": "Trần Thị Bình"},
]

STUDENTS = [
    {"email": "sv01@student.bdu.edu.vn", "student_code": "SV001", "full_name": "Lê Minh Châu"},
    {"email": "sv02@student.bdu.edu.vn", "student_code": "SV002", "full_name": "Phạm Quốc Dũng"},
    {"email": "sv03@student.bdu.edu.vn", "student_code": "SV003", "full_name": "Võ Thị Em"},
    {"email": "sv04@student.bdu.edu.vn", "student_code": "SV004", "full_name": "Đặng Gia Huy"},
]

COURSE = {"course_code": "ITE401", "course_name": "Tiểu luận chuyên ngành CNTT"}

SECTION = {
    "section_code": "ITE401-01",
    "semester": 1,
    "academic_year": "2026-2027",
    "min_members": 1,
    "max_members": 3,
    "pass_threshold": 4.0,
}