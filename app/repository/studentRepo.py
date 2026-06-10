
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Student
from app.schemas.studentSchema import StudentCreate, StudentUpdate
class StudentRepository:
    def __init__(self, session:AsyncSession):
        self.db = session

    async def create_student(self, data:StudentCreate):
        student = Student(**data.model_dump())
        self.db.add(student)
        await self.db.flush()
        return student
    
    async def get_student_by_id(self, student_id:int):
        query=select(Student).where(Student.id==student_id)
        result=await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_student_by_phone(self, phone:str):
        query=select(Student).where(Student.phone==phone)
        result=await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all_students(self):
        query=select(Student)
        result=await self.db.execute(query)
        return result.scalars().all()
    
    async def delete_student(self, student_id:int):
        student=await self.get_student_by_id(student_id)
        if student:
            await self.db.delete(student)
            return True
        return False

    async def update_student(self, student_id:int, data:StudentUpdate):
        student=await self.get_student_by_id(student_id)
        if student:
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(student, key, value)
            await self.db.flush()
            return student
        return None
    