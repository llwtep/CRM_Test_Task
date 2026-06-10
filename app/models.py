from datetime import date, datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Date, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    specialization: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    groups: Mapped[List["Group"]] = relationship(back_populates="teacher")


class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    group_associations: Mapped[List["GroupStudent"]] = relationship(back_populates="student")


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id", ondelete="CASCADE"))
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False) # например: active, finished
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    teacher: Mapped["Teacher"] = relationship(back_populates="groups")
    student_associations: Mapped[List["GroupStudent"]] = relationship(back_populates="group")


class GroupStudent(Base):
    __tablename__ = "group_students"
    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"))
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"))
    joined_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    group: Mapped["Group"] = relationship(back_populates="student_associations")
    student: Mapped["Student"] = relationship(back_populates="group_associations")
    attendances: Mapped[List["Attendance"]] = relationship(back_populates="group_student")


class Attendance(Base):
    __tablename__ = "attendance"
    id: Mapped[int] = mapped_column(primary_key=True)
    group_student_id: Mapped[int] = mapped_column(ForeignKey("group_students.id", ondelete="CASCADE"))
    date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False) 
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    group_student: Mapped["GroupStudent"] = relationship(back_populates="attendances")