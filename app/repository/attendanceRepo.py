
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Attendance
from app.schemas.attendanceSchema import AttendanceCreate, AttendanceUpdate

class AttendanceRepository:
    def __init__(self, session: AsyncSession):
        self.db = session
        
    async def create_attendance(self, data: AttendanceCreate):
        attendance = Attendance(**data.model_dump())
        self.db.add(attendance)
        await self.db.flush()
        return attendance
    
    async def get_attendance_by_id(self, attendance_id: int):
        query = select(Attendance).where(Attendance.id == attendance_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_all_attendances(self):
        query = select(Attendance)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def delete_attendance(self, attendance_id: int):
        attendance = await self.get_attendance_by_id(attendance_id)
        if attendance:
            await self.db.delete(attendance)
            return True
        return False

    async def update_attendance(self, attendance_id: int, data: AttendanceUpdate):
        attendance = await self.get_attendance_by_id(attendance_id)
        if attendance:
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(attendance, key, value)
            await self.db.flush()
            return attendance
        return None
