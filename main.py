from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.api.student_api import router as student_router
from app.api.teacher_api import router as teacher_router
from app.api.group_api import router as group_router
from app.api.group_students_api import router as group_student_router
from app.api.attendance_api import router as attendance_router
from app.api.ai_api import router as ai_router
from app.api.stats_api import router as stats_router

app = FastAPI(title="Educational CRM")

@app.get("/health", status_code=status.HTTP_200_OK, tags=["System"])
async def health_check():
    return {"status": "ok"}

@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )

app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(group_router)
app.include_router(group_student_router)
app.include_router(attendance_router)
app.include_router(ai_router)
app.include_router(stats_router)