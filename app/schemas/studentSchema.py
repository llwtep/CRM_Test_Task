from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class StudentCreate(BaseModel):
    full_name: str = Field(..., description="Full name of the student")
    phone: str = Field(..., description="Phone number of the student")
    birth_date: date = Field(..., description="Student's birth date")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "full_name": "Jane Doe",
                "phone": "+1987654321",
                "birth_date": "2000-01-01"
            }
        }
    )


class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    birth_date: Optional[date] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "full_name": "Jane Doe",
                "phone": "+1987654321",
                "birth_date": "2000-01-01"
            }
        }
    )


class StudentOut(BaseModel):
    id: int
    full_name: str
    phone: str
    birth_date: date
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)