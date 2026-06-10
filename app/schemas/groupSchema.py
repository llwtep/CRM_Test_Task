import enum
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class GroupStatus(str, enum.Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    FROZEN = "frozen"
    COMPLETED = "completed"


class GroupCreate(BaseModel):
    name: str = Field(..., description="Name of the group")
    teacher_id: int = Field(..., description="Teacher ID assigned to the group")
    start_date: date = Field(..., description="Start date of the group")
    status: GroupStatus = Field(..., description="Group status")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Group A",
                "teacher_id": 1,
                "start_date": "2026-06-10",
                "status": "planning"
            }
        }
    )


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    teacher_id: Optional[int] = None
    start_date: Optional[date] = None
    status: Optional[GroupStatus] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Group A",
                "teacher_id": 1,
                "start_date": "2026-06-10",
                "status": "active"
            }
        }
    )

class GroupOut(GroupCreate):
    id: int = Field(..., description="Unique group ID", example=1)
    created_at: datetime = Field(..., description="Timestamp of record creation")

    model_config = ConfigDict(from_attributes=True)
