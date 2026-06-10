from app.repository.statsRepository import StatsRepository


class StatsService:
    def __init__(self, session):
        self.repo = StatsRepository(session)

    async def get_overview(self):
        students, teachers, groups_total, groups_active, attendance_total = (
            await self.repo.get_overview()
        )

        return {
            "students": students,
            "teachers": teachers,
            "groups_total": groups_total,
            "groups_active": groups_active,
            "attendance_records": attendance_total,
        }

    async def get_attendance_stats(self):
        total, present, absent = await self.repo.get_attendance_stats()

        total = total or 1

        return {
            "total": total,
            "present": present or 0,
            "absent": absent or 0,
            "attendance_rate": round((present or 0) / total * 100, 1),
        }

    async def get_groups_stats(self):
        rows = await self.repo.get_groups_stats()

        return [
            {
                "group": r[0],
                "status": r[1],
                "students_count": r[2],
                "present": r[3] or 0,
                "absent": r[4] or 0,
            }
            for r in rows
        ]

    async def get_top_students(self, limit: int, order: str):
        rows = await self.repo.get_top_students(limit, order)

        result = []
        for r in rows:
            total = r[1] or 0
            present = r[2] or 0
            absent = r[3] or 0

            result.append({
                "student": r[0],
                "total": total,
                "present": present,
                "absent": absent,
                "attendance_rate": round(present / total * 100, 1) if total else 0,
            })

        return result