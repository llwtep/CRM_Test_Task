import enum
from datetime import date as date_type, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class AttendanceStatusEnum(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"


class AttendanceCreate(BaseModel):
    group_student_id: int = Field(..., description="ID of the student in the group")
    date: date_type = Field(..., description="Date of attendance")
    status: AttendanceStatusEnum = Field(
        default=AttendanceStatusEnum.PRESENT,
        description="Attendance status",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "group_student_id": 1,
                "date": "2026-06-10",
                "status": "present"
            }
        }
    )

class AttendanceUpdate(BaseModel):
    group_student_id: Optional[int] = None
    date: Optional[date_type] = None
    status: Optional[AttendanceStatusEnum] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "group_student_id": 1,
                "date": "2026-06-10",
                "status": "absent"
            }
        }
    )

class AttendanceOut(BaseModel):
    id: int
    group_student_id: int
    date: date_type
    status: AttendanceStatusEnum
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)