
from app.repository.teacherRepo import TeacherRepository
from app.schemas.teacherSchema import TeacherCreate, TeacherUpdate, TeacherOut
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.exceptions import NotFoundException, ValidationException

class TeacherService:
    def __init__(self,session:AsyncSession):
        self.db=session
        self.teacher_repo=TeacherRepository(session)

    async def create_teacher(self,data:TeacherCreate)->TeacherOut:
        async with self.db.begin():
            existing_teacher = await self.teacher_repo.get_teacher_by_phone(data.phone)
            if existing_teacher:
                raise ValidationException(
                    f"Teacher with phone {data.phone} is already registered."
                )
        
            teacher= await self.teacher_repo.create_teacher(data)
        await self.db.refresh(teacher)
        return TeacherOut.model_validate(teacher)
    
    async def get_teacher_by_id(self,teacher_id:int)->TeacherOut|None:
        teacher= await self.teacher_repo.get_teacher_by_id(teacher_id)
        return TeacherOut.model_validate(teacher) if teacher else None

    async def get_all_teachers(self)->list[TeacherOut]:
        teachers= await self.teacher_repo.get_all_teachers()
        return [TeacherOut.model_validate(teacher) for teacher in teachers]

    async def delete_teacher(self,teacher_id:int)->bool:
        async with self.db.begin():
            return await self.teacher_repo.delete_teacher(teacher_id)
    
    async def update_teacher(self,teacher_id:int,data:TeacherUpdate)->TeacherOut|None:
        async with self.db.begin():
            current_teacher = await self.teacher_repo.get_teacher_by_id(teacher_id)
            if not current_teacher:
                raise NotFoundException(f"Teacher with id {teacher_id} does not exist.")
        
            teacher= await self.teacher_repo.update_teacher(teacher_id,data)
        await self.db.refresh(teacher)
        return TeacherOut.model_validate(teacher) if teacher else None