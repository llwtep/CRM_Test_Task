

from app.repository.attendanceRepo import AttendanceRepository
from app.repository.groupStudentRepo import GroupStudentRepository
from app.schemas.attendanceSchema import AttendanceCreate, AttendanceUpdate, AttendanceOut
from app.schemas.groupStudentSchema import GroupStudentStatus
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.exceptions import NotFoundException, ValidationException

class AttendanceService:
    def __init__(self, session: AsyncSession):
        self.db = session
        self.attendance_repo = AttendanceRepository(session)
        self.group_student_repo=GroupStudentRepository(session)
    
    async def create_attendance(self, data: AttendanceCreate) -> AttendanceOut:
        async with self.db.begin():
            group_student = await self.group_student_repo.get_group_student_by_id(data.group_student_id)
            if not group_student:
                raise NotFoundException(f"GroupStudent with id {data.group_student_id} does not exist.")
            
            if group_student.status != GroupStudentStatus.ACTIVE:
                raise ValidationException(f"Cannot create attendance for a {group_student.status} status.")
        
            attendance = await self.attendance_repo.create_attendance(data)

        return AttendanceOut.model_validate(attendance)
    
    async def get_attendance_by_id(self, attendance_id: int) -> AttendanceOut | None:
        attendance = await self.attendance_repo.get_attendance_by_id(attendance_id)
        return AttendanceOut.model_validate(attendance) if attendance else None
    
    async def get_all_attendances(self) -> list[AttendanceOut]: 
        attendances = await self.attendance_repo.get_all_attendances()
        return [AttendanceOut.model_validate(attendance) for attendance in attendances]
    
    async def delete_attendance(self, attendance_id: int) -> bool:
        async with self.db.begin():
            return await self.attendance_repo.delete_attendance(attendance_id)
    
    async def update_attendance(self, attendance_id: int, data: AttendanceUpdate) -> AttendanceOut | None:
        async with self.db.begin():
            group_student = await self.group_student_repo.get_group_student_by_id(data.group_student_id)
            if not group_student:
                raise NotFoundException(f"GroupStudent with id {data.group_student_id} does not exist.")
            if group_student.status != GroupStudentStatus.ACTIVE:
                raise ValidationException(f"Cannot update attendance for a {group_student.status} status.")
        
            attendance = await self.attendance_repo.update_attendance(attendance_id, data)
        return AttendanceOut.model_validate(attendance) if attendance else None