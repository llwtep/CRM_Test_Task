from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TeacherCreate(BaseModel):
    full_name: str = Field(..., description="Full name of the teacher")
    phone: str = Field(..., description="Phone number of the teacher")
    specialization: Optional[str] = Field(None, description="Teacher's specialization area")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "full_name": "John Doe",
                "phone": "+1234567890",
                "specialization": "Mathematics"
            }
        }
    )


class TeacherUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    specialization: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "full_name": "John Doe",
                "phone": "+1234567890",
                "specialization": "Physics"
            }
        }
    )


class TeacherOut(BaseModel):
    id: int
    full_name: str
    phone: str
    specialization: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)