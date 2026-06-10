from app.repository.groupRepo import GroupRepository
from app.repository.groupStudentRepo import GroupStudentRepository
from app.repository.studentRepo import StudentRepository
from app.repository.teacherRepo import TeacherRepository
from app.schemas.groupSchema import GroupStatus
from app.schemas.groupStudentSchema import GroupStudentCreate, GroupStudentUpdate, GroupStudentOut
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.exceptions import NotFoundException, ValidationException

class GroupStudentService:
    def __init__(self, session:AsyncSession):
        self.db = session
        self.group_repo = GroupRepository(session)
        self.teacher_repo=TeacherRepository(session)
        self.student_repo=StudentRepository(session)
        self.group_student_repo=GroupStudentRepository(session)
    
    async def create_group_student(self, data: GroupStudentCreate)->GroupStudentOut:
        async with self.db.begin():
            group = await self.group_repo.get_group_by_id(data.group_id)
            if not group:
                raise NotFoundException(f"Group with id {data.group_id} does not exist.")
        
            student = await self.student_repo.get_student_by_id(data.student_id)
            if not student:
                raise NotFoundException(f"Student with id {data.student_id} does not exist.")
        
            group_student = await self.group_student_repo.create_group_student(data)
        return GroupStudentOut.model_validate(group_student)
    
    async def get_group_student_by_id(self, group_student_id: int)->GroupStudentOut|None:
        group_student = await self.group_student_repo.get_group_student_by_id(group_student_id)
        return GroupStudentOut.model_validate(group_student) if group_student else None
    
    async def get_all_group_students(self)->list[GroupStudentOut]:
        group_students = await self.group_student_repo.get_all_group_students()
        return [GroupStudentOut.model_validate(group_student) for group_student in group_students]
    
    async def delete_group_student(self, group_student_id: int)->bool:
        async with self.db.begin():
            return await self.group_student_repo.delete_group_student(group_student_id) 
    
    async def update_group_student(self, group_student_id: int, data: GroupStudentUpdate)->GroupStudentOut|None:
        async with self.db.begin():
            group = await self.group_repo.get_group_by_id(data.group_id)
            if not group:
                raise NotFoundException(f"Group with id {data.group_id} does not exist.")
        
            student = await self.student_repo.get_student_by_id(data.student_id)
            if not student:
                raise NotFoundException(f"Student with id {data.student_id} does not exist.")
            if group.status==GroupStatus.COMPLETED:
                raise ValidationException("Cannot update a completed group.")
            group_student = await self.group_student_repo.update_group_student(group_student_id, data)
        return GroupStudentOut.model_validate(group_student) if group_student else None