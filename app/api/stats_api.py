from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.services.statsService import StatsService
from app.schemas.statsSchema import (
    AttendanceStatsOut,
    GroupStatsOut,
    StudentTopOut,
    OverviewOut,
)

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/overview", response_model=OverviewOut)
async def get_overview(db: AsyncSession = Depends(get_db)):
    service = StatsService(db)
    return await service.get_overview()


@router.get("/attendance", response_model=AttendanceStatsOut)
async def get_attendance_stats(db: AsyncSession = Depends(get_db)):
    service = StatsService(db)
    return await service.get_attendance_stats()


@router.get("/groups", response_model=list[GroupStatsOut])
async def get_groups_stats(db: AsyncSession = Depends(get_db)):
    service = StatsService(db)
    return await service.get_groups_stats()


@router.get("/students/top", response_model=list[StudentTopOut])
async def get_top_students(
    limit: int = 10,
    order: str = "best",
    db: AsyncSession = Depends(get_db),
):
    service = StatsService(db)
    return await service.get_top_students(limit, order)