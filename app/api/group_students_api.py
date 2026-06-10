from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.services.groupStudentService import GroupStudentService
from app.schemas.groupStudentSchema import GroupStudentCreate, GroupStudentUpdate, GroupStudentOut
from app.services.exceptions import NotFoundException, ValidationException

router = APIRouter(prefix="/group-students", tags=["GroupStudents"])

@router.post("/", response_model=GroupStudentOut, status_code=status.HTTP_201_CREATED, summary="Create group-student relationship", description="Assigns a student to a group.")
async def create_group_student(group_student: GroupStudentCreate, session: AsyncSession = Depends(get_db)):
    service = GroupStudentService(session)
    try:
        return await service.create_group_student(group_student)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=list[GroupStudentOut], summary="Get all group-student relationships", description="Retrieves a list of all group-student assignments.")
async def get_all_group_students(session: AsyncSession = Depends(get_db)):
    service = GroupStudentService(session)
    return await service.get_all_group_students()

@router.get("/{group_student_id}", response_model=GroupStudentOut, summary="Get group-student by ID", description="Retrieves a specific group-student assignment by its unique ID.")
async def get_group_student(group_student_id: int, session: AsyncSession = Depends(get_db)):
    service = GroupStudentService(session)
    try:
        group_student = await service.get_group_student_by_id(group_student_id)
        if not group_student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group-Student relationship not found")
        return group_student
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{group_student_id}", response_model=GroupStudentOut, summary="Update group-student assignment", description="Updates an existing group-student assignment.")
async def update_group_student(group_student_id: int, group_student: GroupStudentUpdate, session: AsyncSession = Depends(get_db)):
    service = GroupStudentService(session)
    try:
        updated_group_student = await service.update_group_student(group_student_id, group_student)
        if not updated_group_student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group-Student relationship not found")
        return updated_group_student
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{group_student_id}", response_model=bool, summary="Delete group-student assignment", description="Deletes a group-student assignment by its unique ID.")
async def delete_group_student(group_student_id: int, session: AsyncSession = Depends(get_db)):
    service = GroupStudentService(session)
    try:
        success = await service.delete_group_student(group_student_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group-Student relationship not found")
        return success
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
