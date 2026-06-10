from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case

from app.models import Student, Teacher, Group, GroupStudent, Attendance


class StatsRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_overview(self):
        students = await self.db.scalar(select(func.count(Student.id)))
        teachers = await self.db.scalar(select(func.count(Teacher.id)))
        groups_total = await self.db.scalar(select(func.count(Group.id)))
        groups_active = await self.db.scalar(
            select(func.count(Group.id)).where(Group.status == "active")
        )
        attendance_total = await self.db.scalar(select(func.count(Attendance.id)))

        return students, teachers, groups_total, groups_active, attendance_total

    async def get_attendance_stats(self):
        result = await self.db.execute(
            select(
                func.count(Attendance.id),
                func.sum(case((Attendance.status == "present", 1), else_=0)),
                func.sum(case((Attendance.status == "absent", 1), else_=0)),
            )
        )
        return result.fetchone()

    async def get_groups_stats(self):
        result = await self.db.execute(
            select(
                Group.name,
                Group.status,
                func.count(GroupStudent.id),
                func.sum(case((Attendance.status == "present", 1), else_=0)),
                func.sum(case((Attendance.status == "absent", 1), else_=0)),
            )
            .join(GroupStudent, GroupStudent.group_id == Group.id, isouter=True)
            .join(Attendance, Attendance.group_student_id == GroupStudent.id, isouter=True)
            .group_by(Group.id, Group.name, Group.status)
        )
        return result.fetchall()

    async def get_top_students(self, limit: int, order: str):
        present = func.sum(case((Attendance.status == "present", 1), else_=0))
        absent = func.sum(case((Attendance.status == "absent", 1), else_=0))

        sort_by = present if order == "best" else absent

        result = await self.db.execute(
            select(
                Student.full_name,
                func.count(Attendance.id),
                present,
                absent,
            )
            .join(GroupStudent, GroupStudent.student_id == Student.id)
            .join(Attendance, Attendance.group_student_id == GroupStudent.id)
            .group_by(Student.id, Student.full_name)
            .order_by(sort_by.desc())
            .limit(limit)
        )
        return result.fetchall()