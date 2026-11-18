from pydantic import BaseModel


class ClassReportRow(BaseModel):
    lop_id: int
    ma_lop: str
    ten_mon: str
    giang_vien: str
    so_sinh_vien: int
    tong_ho_so: int
    cho_duyet: int
    da_duyet: int
    tu_choi: int


class ClassSummaryReport(BaseModel):
    mode: str            # "blocking" | "async"
    delay_seconds: float
    elapsed_ms: int
    rows: list[ClassReportRow]