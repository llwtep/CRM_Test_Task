
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Group
from app.schemas.groupSchema import GroupCreate, GroupUpdate

class GroupRepository:
    def __init__(self, session: AsyncSession):
        self.db = session
        
    async def create_group(self, data: GroupCreate):
        group = Group(**data.model_dump())
        self.db.add(group)
        await self.db.flush()
        return group
    
    async def get_group_by_id(self, group_id: int):
        query = select(Group).where(Group.id == group_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_all_groups(self):
        query = select(Group)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def delete_group(self, group_id: int):
        group = await self.get_group_by_id(group_id)
        if group:
            await self.db.delete(group)
            return True
        return False

    async def update_group(self, group_id: int, data: GroupUpdate):
        group = await self.get_group_by_id(group_id)
        if group:
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(group, key, value)
            await self.db.flush()
            return group
        return None
