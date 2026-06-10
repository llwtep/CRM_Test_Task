from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.services.teacherService import TeacherService
from app.schemas.teacherSchema import TeacherCreate, TeacherUpdate, TeacherOut
from app.services.exceptions import NotFoundException, ValidationException

router = APIRouter(prefix="/teachers", tags=["Teachers"])

@router.post("/", response_model=TeacherOut, status_code=status.HTTP_201_CREATED, summary="Create a new teacher", description="Registers a new teacher in the system.")
async def create_teacher(teacher: TeacherCreate, session: AsyncSession = Depends(get_db)):
    service = TeacherService(session)
    try:
        return await service.create_teacher(teacher)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=list[TeacherOut], summary="Get all teachers", description="Retrieves a list of all registered teachers.")
async def get_all_teachers(session: AsyncSession = Depends(get_db)):
    service = TeacherService(session)
    return await service.get_all_teachers()

@router.get("/{teacher_id}", response_model=TeacherOut, summary="Get teacher by ID", description="Retrieves a specific teacher by their unique ID.")
async def get_teacher(teacher_id: int, session: AsyncSession = Depends(get_db)):
    service = TeacherService(session)
    try:
        teacher = await service.get_teacher_by_id(teacher_id)
        if not teacher:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
        return teacher
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{teacher_id}", response_model=TeacherOut, summary="Update teacher", description="Updates the details of an existing teacher.")
async def update_teacher(teacher_id: int, teacher: TeacherUpdate, session: AsyncSession = Depends(get_db)):
    service = TeacherService(session)
    try:
        updated_teacher = await service.update_teacher(teacher_id, teacher)
        if not updated_teacher:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
        return updated_teacher
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{teacher_id}", response_model=bool, summary="Delete teacher", description="Deletes a teacher by their unique ID.")
async def delete_teacher(teacher_id: int, session: AsyncSession = Depends(get_db)):
    service = TeacherService(session)
    try:
        success = await service.delete_teacher(teacher_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
        return success
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
