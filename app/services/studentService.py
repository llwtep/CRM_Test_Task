from app.repository.studentRepo import StudentRepository
from app.schemas.studentSchema import StudentCreate, StudentUpdate, StudentOut

from sqlalchemy.ext.asyncio import AsyncSession
from app.services.exceptions import NotFoundException, ValidationException

class StudentService:
    def __init__(self, session: AsyncSession):
        self.db=session
        self.student_repo=StudentRepository(session)

    async def create_student(self,data:StudentCreate)->StudentOut:
        async with self.db.begin():
            existing_student = await self.student_repo.get_student_by_phone(data.phone)
            if existing_student:
                raise ValidationException(
                    f"Student with phone {data.phone} is already registered."
                )
            
            student = await self.student_repo.create_student(data)
            
        await self.db.refresh(student)
        return StudentOut.model_validate(student)
    
    async def get_student_by_id(self,student_id:int)->StudentOut|None:
        student= await self.student_repo.get_student_by_id(student_id)
        return StudentOut.model_validate(student) if student else None
    
    async def get_all_students(self)->list[StudentOut]:
        students= await self.student_repo.get_all_students()
        return [StudentOut.model_validate(student) for student in students]
    
    async def delete_student(self,student_id:int)->bool:
        async with self.db.begin():
            success = await self.student_repo.delete_student(student_id)
        return success
    
    async def update_student(self,student_id:int,data:StudentUpdate)->StudentOut|None:
        async with self.db.begin():
            current_student = await self.student_repo.get_student_by_id(student_id)
            if not current_student:
                raise NotFoundException(f"Student with id {student_id} does not exist.")
        
            student = await self.student_repo.update_student(student_id, data)
        await self.db.refresh(student)
        return StudentOut.model_validate(student)