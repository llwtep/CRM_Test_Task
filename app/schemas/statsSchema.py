from pydantic import BaseModel


class OverviewOut(BaseModel):
    students: int
    teachers: int
    groups_total: int
    groups_active: int
    attendance_records: int


class AttendanceStatsOut(BaseModel):
    total: int
    present: int
    absent: int
    attendance_rate: float


class GroupStatsOut(BaseModel):
    group: str
    status: str
    students_count: int
    present: int
    absent: int


class StudentTopOut(BaseModel):
    student: str
    total: int
    present: int
    absent: int
    attendance_rate: float