"""SQLAlchemy models for the 8 core tables.

The tables already exist in Supabase, so DO NOT call Base.metadata.create_all().
These classes only describe the tables so Python can read and write them.
If you change a table in Supabase, change it here too.
"""

from sqlalchemy import (
    Column, Integer, SmallInteger, String, Boolean, DateTime,
    ForeignKey, UniqueConstraint, func,
)
from sqlalchemy.orm import relationship

from database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    code = Column(String(10), unique=True, nullable=False)   # CS, EC, ME
    name = Column(String(100), nullable=False)
    hod_teacher_id = Column(Integer, ForeignKey("teachers.id"), unique=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    login_id = Column(String(30), unique=True)
    password_hash = Column(String, nullable=False)
    role = Column(String(10), nullable=False)   # student / teacher / hod / principal
    full_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="user", uselist=False)
    teacher = relationship("Teacher", back_populates="user", uselist=False)


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    designation = Column(String(50))

    user = relationship("User", back_populates="teacher")
    # departments <-> teachers has two links (department + HOD),
    # so we say exactly which column this relationship uses.
    department = relationship("Department", foreign_keys=[department_id])


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    roll_no = Column(String(20), unique=True, nullable=False)
    current_sem = Column(SmallInteger, nullable=False)
    batch_year = Column(SmallInteger, nullable=False)

    user = relationship("User", back_populates="student")
    department = relationship("Department")


class Term(Base):
    __tablename__ = "terms"

    id = Column(Integer, primary_key=True)
    academic_year = Column(String(9), nullable=False)   # 2024-25
    name = Column(String(30), nullable=False)           # Monsoon
    is_current = Column(Boolean, nullable=False, default=False)


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    code = Column(String(10), unique=True, nullable=False)   # CS301
    name = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    semester_no = Column(SmallInteger, nullable=False)
    credits = Column(SmallInteger, nullable=False, default=4)

    department = relationship("Department")


class CourseOffering(Base):
    __tablename__ = "course_offerings"
    __table_args__ = (UniqueConstraint("subject_id", "teacher_id", "term_id"),)

    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    term_id = Column(Integer, ForeignKey("terms.id"), nullable=False)

    subject = relationship("Subject")
    teacher = relationship("Teacher")
    term = relationship("Term")


class Enrollment(Base):
    __tablename__ = "enrollments"
    __table_args__ = (UniqueConstraint("student_id", "offering_id"),)

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    offering_id = Column(Integer, ForeignKey("course_offerings.id"), nullable=False)

    student = relationship("Student")
    offering = relationship("CourseOffering")