from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.services.studentService import StudentService
from app.schemas.studentSchema import StudentCreate, StudentUpdate, StudentOut
from app.services.exceptions import NotFoundException, ValidationException

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=StudentOut, status_code=status.HTTP_201_CREATED, summary="Create a new student", description="Registers a new student in the system.")
async def create_student(student_data: StudentCreate, db: AsyncSession = Depends(get_db)):
    service = StudentService(db)
    try:
        return await service.create_student(student_data)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{student_id}", response_model=StudentOut, summary="Get student by ID", description="Retrieves a specific student by their unique ID.")
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    service = StudentService(db)
    try:
        student = await service.get_student_by_id(student_id)
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        return student
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=list[StudentOut], summary="Get all students", description="Retrieves a list of all registered students.")
async def get_all_students(db: AsyncSession = Depends(get_db)):
    service = StudentService(db)
    return await service.get_all_students()

@router.delete("/{student_id}", response_model=bool, summary="Delete student", description="Deletes a student by their unique ID.")
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):  
    service = StudentService(db)
    try:
        success = await service.delete_student(student_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        return success
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{student_id}", response_model=StudentOut, summary="Update student", description="Updates the details of an existing student.")
async def update_student(student_id: int, student_data: StudentUpdate, db: AsyncSession = Depends(get_db)):
    service = StudentService(db)
    try:
        updated_student = await service.update_student(student_id, student_data)
        if not updated_student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        return updated_student
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
