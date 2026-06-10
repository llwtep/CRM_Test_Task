
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Teacher
from app.schemas.teacherSchema import TeacherCreate, TeacherUpdate

class TeacherRepository:
    def __init__(self, session: AsyncSession):
        self.db = session
        
    async def create_teacher(self, data: TeacherCreate):
        teacher = Teacher(**data.model_dump())
        self.db.add(teacher)
        await self.db.flush()
        return teacher
    
    async def get_teacher_by_id(self, teacher_id: int):
        query = select(Teacher).where(Teacher.id == teacher_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    async def get_teacher_by_phone(self, phone:str):
        query=select(Teacher).where(Teacher.phone==phone)
        result=await self.db.execute(query)
        return result.scalar_one_or_none()
    async def get_all_teachers(self):
        query = select(Teacher)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def delete_teacher(self, teacher_id: int):
        teacher = await self.get_teacher_by_id(teacher_id)
        if teacher:
            await self.db.delete(teacher)
            return True
        return False

    async def update_teacher(self, teacher_id: int, data: TeacherUpdate):
        teacher = await self.get_teacher_by_id(teacher_id)
        if teacher:
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(teacher, key, value)
            await self.db.flush()
            return teacher
        return None
