from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession 
from app.db import get_db
from app.services.groupService import GroupService
from app.schemas.groupSchema import GroupCreate, GroupUpdate, GroupOut
from app.services.exceptions import NotFoundException, ValidationException

router = APIRouter(prefix="/groups", tags=["Groups"])

@router.post("/", response_model=GroupOut, status_code=status.HTTP_201_CREATED, summary="Create a new group", description="Registers a new group in the system.")
async def create_group(group: GroupCreate, session: AsyncSession = Depends(get_db)):
    service = GroupService(session)
    try:
        return await service.create_group(group)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=list[GroupOut], summary="Get all groups", description="Retrieves a list of all registered groups.")
async def get_all_groups(session: AsyncSession = Depends(get_db)):
    service = GroupService(session)
    return await service.get_all_groups()

@router.get("/{group_id}", response_model=GroupOut, summary="Get group by ID", description="Retrieves a specific group by its unique ID.")
async def get_group(group_id: int, session: AsyncSession = Depends(get_db)):
    service = GroupService(session)
    try:
        group = await service.get_group_by_id(group_id)
        if not group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
        return group
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{group_id}", response_model=GroupOut, summary="Update group", description="Updates the details of an existing group.")
async def update_group(group_id: int, group: GroupUpdate, session: AsyncSession = Depends(get_db)):
    service = GroupService(session)
    try:
        updated_group = await service.update_group(group_id, group)
        if not updated_group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
        return updated_group
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{group_id}", response_model=bool, summary="Delete group", description="Deletes a group by its unique ID.")
async def delete_group(group_id: int, session: AsyncSession = Depends(get_db)):
    service = GroupService(session)
    try:
        success = await service.delete_group(group_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
        return success
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
