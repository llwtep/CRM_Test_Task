from datetime import datetime
import enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class GroupStudentStatus(str, enum.Enum):
    ACTIVE = "active"
    LEFT = "left"
    FROZEN = "frozen"
    COMPLETED = "completed"


class GroupStudentCreate(BaseModel):
    group_id: int = Field(..., description="ID of the group")
    student_id: int = Field(..., description="ID of the student")
    status: GroupStudentStatus = Field(..., description="Status of the student in the group")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "group_id": 1,
                "student_id": 1,
                "status": "active"
            }
        }
    )


class GroupStudentUpdate(BaseModel):
    group_id: Optional[int] = None
    student_id: Optional[int] = None
    status: Optional[GroupStudentStatus] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "group_id": 1,
                "student_id": 1,
                "status": "frozen"
            }
        }
    )


class GroupStudentOut(BaseModel):
    id: int
    group_id: int
    student_id: int
    status: GroupStudentStatus
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)