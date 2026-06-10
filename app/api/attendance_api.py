from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.services.attendanceService import AttendanceService
from app.schemas.attendanceSchema import AttendanceCreate, AttendanceUpdate, AttendanceOut  
from app.services.exceptions import NotFoundException, ValidationException

router = APIRouter(prefix="/attendances", tags=["Attendances"])

@router.post("/", response_model=AttendanceOut, status_code=status.HTTP_201_CREATED, summary="Create attendance record", description="Records attendance for a student in a group.")
async def create_attendance(attendance: AttendanceCreate, session: AsyncSession = Depends(get_db)):
    service = AttendanceService(session)
    try:
        return await service.create_attendance(attendance)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=list[AttendanceOut], summary="Get all attendance records", description="Retrieves a list of all recorded attendance.")
async def get_all_attendances(session: AsyncSession = Depends(get_db)):
    service = AttendanceService(session)
    return await service.get_all_attendances()

@router.get("/{attendance_id}", response_model=AttendanceOut, summary="Get attendance by ID", description="Retrieves a specific attendance record by its unique ID.")
async def get_attendance(attendance_id: int, session: AsyncSession = Depends(get_db)):
    service = AttendanceService(session)
    try:
        attendance = await service.get_attendance_by_id(attendance_id)
        if not attendance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance not found")
        return attendance
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{attendance_id}", response_model=AttendanceOut, summary="Update attendance", description="Updates an existing attendance record.")
async def update_attendance(attendance_id: int, attendance: AttendanceUpdate, session: AsyncSession = Depends(get_db)):
    service = AttendanceService(session)
    try:
        updated_attendance = await service.update_attendance(attendance_id, attendance)
        if not updated_attendance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance not found")
        return updated_attendance
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{attendance_id}", response_model=bool, summary="Delete attendance", description="Deletes an attendance record by its unique ID.")
async def delete_attendance(attendance_id: int, session: AsyncSession = Depends(get_db)):
    service = AttendanceService(session)
    try:
        success = await service.delete_attendance(attendance_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance not found")
        return success
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
