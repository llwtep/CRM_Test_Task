
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import GroupStudent
from app.schemas.groupStudentSchema import GroupStudentCreate, GroupStudentUpdate

class GroupStudentRepository:
    def __init__(self, session: AsyncSession):
        self.db = session
        
    async def create_group_student(self, data: GroupStudentCreate):
        group_student = GroupStudent(**data.model_dump())
        self.db.add(group_student)
        await self.db.flush()
        return group_student
    
    async def get_group_student_by_id(self, group_student_id: int):
        query = select(GroupStudent).where(GroupStudent.id == group_student_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_all_group_students(self):
        query = select(GroupStudent)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def delete_group_student(self, group_student_id: int):
        group_student = await self.get_group_student_by_id(group_student_id)
        if group_student:
            await self.db.delete(group_student)
            return True
        return False

    async def update_group_student(self, group_student_id: int, data: GroupStudentUpdate):
        group_student = await self.get_group_student_by_id(group_student_id)
        if group_student:
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(group_student, key, value)
            await self.db.flush()
            return group_student
        return None
