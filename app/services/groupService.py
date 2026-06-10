
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.groupRepo import GroupRepository
from app.repository.teacherRepo import TeacherRepository
from app.schemas.groupSchema import GroupCreate, GroupUpdate, GroupOut, GroupStatus
from app.services.exceptions import NotFoundException, ValidationException

class GroupService:
    def __init__(self, session: AsyncSession):
        self.db = session
        self.group_repo = GroupRepository(session)
        self.teacher_repo=TeacherRepository(session)
    
    async def create_group(self, data: GroupCreate) -> GroupOut:
        async with self.db.begin():
            teacher = await self.teacher_repo.get_teacher_by_id(data.teacher_id)
            if not teacher:
                raise NotFoundException(f"Teacher with id {data.teacher_id} does not exist.")
        
            group = await self.group_repo.create_group(data)
        await self.db.refresh(group)
        return GroupOut.model_validate(group)
    
    async def get_group_by_id(self, group_id: int) -> GroupOut | None:
        group = await self.group_repo.get_group_by_id(group_id)
        return GroupOut.model_validate(group) if group else None
    
    async def get_all_groups(self) -> list[GroupOut]:
        groups = await self.group_repo.get_all_groups()
        return [GroupOut.model_validate(group) for group in groups]
    
    async def delete_group(self, group_id: int) -> bool:
        async with self.db.begin():
            success = await self.group_repo.delete_group(group_id)
        return success
    
    async def update_group(self, group_id: int, data: GroupUpdate) -> GroupOut | None:
        async with self.db.begin():
            group = await self.group_repo.get_group_by_id(group_id)
            if not group:
                raise NotFoundException(f"Group with id {group_id} does not exist.")
            if group.status == GroupStatus.COMPLETED:
                raise ValidationException("Cannot update a completed group.")
            if data.teacher_id is not None:
                teacher = await self.teacher_repo.get_teacher_by_id(data.teacher_id)
                if not teacher:
                    raise NotFoundException(f"Teacher with id {data.teacher_id} does not exist.")
        
            new_group = await self.group_repo.update_group(group_id, data)
        if new_group:
            await self.db.refresh(new_group)
            return GroupOut.model_validate(new_group)
        return None

    