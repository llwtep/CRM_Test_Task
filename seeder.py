import asyncio
import random
from datetime import date
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_session_factory
from app.schemas.teacherSchema import TeacherCreate
from app.schemas.studentSchema import StudentCreate
from app.schemas.groupSchema import GroupCreate, GroupStatus
from app.schemas.groupStudentSchema import GroupStudentCreate
from app.schemas.groupStudentSchema import GroupStudentStatus
from app.schemas.attendanceSchema import AttendanceCreate, AttendanceStatusEnum

from app.repository.teacherRepo import TeacherRepository
from app.repository.studentRepo import StudentRepository
from app.repository.groupRepo import GroupRepository
from app.repository.groupStudentRepo import GroupStudentRepository
from app.repository.attendanceRepo import AttendanceRepository


fake = Faker('ru_RU')

specializations = [
    "Mathematics",
    "English",
    "Computer Science",
    "History",
    "Physics"
]

attendance_statuses = [AttendanceStatusEnum.PRESENT, AttendanceStatusEnum.ABSENT]


async def seed_teachers(session: AsyncSession, count: int = 5):
    repo = TeacherRepository(session)
    teachers = []
    used_phones = set()
    
    for _ in range(count):
        while True:
            phone = fake.phone_number()[:15]
            if phone not in used_phones:
                used_phones.add(phone)
                break
        
        teacher_data = TeacherCreate(
            full_name=fake.name(),
            phone=phone,
            specialization=random.choice(specializations)
        )
        try:
            teacher = await repo.create_teacher(teacher_data)
            await session.flush()
            teachers.append(teacher)
        except Exception as e:
            pass
    
    return teachers


async def seed_students(session: AsyncSession, count: int = 20):
    repo = StudentRepository(session)
    students = []
    used_phones = set()
    
    for _ in range(count):
        while True:
            phone = fake.phone_number()[:15]
            if phone not in used_phones:
                used_phones.add(phone)
                break
        
        birth_date = fake.date_between(start_date='-25y', end_date='-16y')
        student_data = StudentCreate(
            full_name=fake.name(),
            phone=phone,
            birth_date=birth_date
        )
        try:
            student = await repo.create_student(student_data)
            await session.flush()
            students.append(student)
        except Exception as e:
            await session.rollback()
    
    return students


async def seed_groups(session: AsyncSession, teachers: list, count: int = 10):
    repo = GroupRepository(session)
    groups = []

    statuses = (
        [GroupStatus.ACTIVE] * 6 + 
        [GroupStatus.PLANNING] * 2 + 
        [GroupStatus.FROZEN] * 1 + 
        [GroupStatus.COMPLETED] * 1
    )
    
    for i in range(count):
        teacher = random.choice(teachers)
        status = statuses[i]
        
        if status == GroupStatus.PLANNING:
            start_date = fake.date_between(start_date='today', end_date='+30d')
        else:
            start_date = fake.date_between(start_date='-150d', end_date='-30d')
            
        group_data = GroupCreate(
            name=f"Group {fake.word().capitalize()}-{random.randint(10,99)}",
            teacher_id=teacher.id,
            start_date=start_date,
            status=status
        )
        try:
            group = await repo.create_group(group_data)
            await session.flush()
            groups.append(group)
        except Exception as e:
            await session.rollback()
    
    return groups


async def seed_group_students(session: AsyncSession, groups: list, students: list):
    repo = GroupStudentRepository(session)
    group_students = []
    
    student_statuses = [GroupStudentStatus.ACTIVE] * 8 + [GroupStudentStatus.LEFT] * 1 + [GroupStudentStatus.FROZEN] * 1

    for group in groups:
        num_students = random.randint(4, 10)
        selected_students = random.sample(students, min(num_students, len(students)))
        
        for student in selected_students:
            if group.status == GroupStatus.COMPLETED:
                status = GroupStudentStatus.COMPLETED
            elif group.status == GroupStatus.PLANNING:
                status = GroupStudentStatus.ACTIVE
            else:
                status = random.choice(student_statuses)

            group_student_data = GroupStudentCreate(
                group_id=group.id,
                student_id=student.id,
                status=status
            )
            try:
                group_student = await repo.create_group_student(group_student_data)
                await session.flush()
                group_students.append(group_student)
            except Exception as e:
                await session.rollback()
    
    return group_students


async def seed_attendances(session: AsyncSession, group_students: list, count: int = 100):
    repo = AttendanceRepository(session)
    attendances = []
    
    valid_appointments = [
        gs for gs in group_students 
        if gs.status in [GroupStudentStatus.ACTIVE, GroupStudentStatus.COMPLETED]
    ]

    if not valid_appointments:
        print("No valid students for attendance generation!")
        return attendances

    attempts = 0
    while len(attendances) < count and attempts < count * 3:
        attempts += 1
        group_student = random.choice(valid_appointments)
        
        attendance_date = fake.date_between(start_date='-2m', end_date='today')
        
        attendance_data = AttendanceCreate(
            group_student_id=group_student.id,
            date=attendance_date,
            status=random.choice(attendance_statuses)
        )
        try:
            attendance = await repo.create_attendance(attendance_data)
            await session.flush()
            attendances.append(attendance)
        except Exception as e:
            await session.rollback()
    
    return attendances


async def run_seeder():
    async with async_session_factory() as session:
        try:
            print("Creating teachers...")
            teachers = await seed_teachers(session, 5)
            print(f"Created {len(teachers)} teachers")
            
            print("Creating students...")
            students = await seed_students(session, 20)
            print(f"Created {len(students)} students")
            
            print("Creating groups...")
            groups = await seed_groups(session, teachers, 10)
            print(f"Created {len(groups)} groups")
            
            print("Creating group-student associations...")
            group_students = await seed_group_students(session, groups, students)
            print(f"Created {len(group_students)} group-student associations")
            
            print("Creating attendance records...")
            attendances = await seed_attendances(session, group_students, 100)
            print(f"Created {len(attendances)} attendance records")
            
            await session.commit()
            print("Seeding completed successfully!")
        except Exception as e:
            await session.rollback()
            print(f"Seeding failed: {e}")


if __name__ == "__main__":
    asyncio.run(run_seeder())
