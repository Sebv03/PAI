# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class UserRole(str, enum.Enum):
    ESTUDIANTE = "estudiante"
    DOCENTE = "docente"
    PSICOPEDAGOGO = "psicopedagogo"
    ADMINISTRADOR = "administrador"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column("nombre_completo", String(100), index=True)
    correo = Column("correo", String(100), unique=True, index=True, nullable=False)
    contraseña_hash = Column("contraseña_hash", String(255), nullable=False)
    activo = Column("activo", Boolean, default=True)
    
    # --- ¡CRÍTICO! Este es el campo 'rol' ---
    rol = Column("rol", Enum(UserRole), default=UserRole.ESTUDIANTE, nullable=False)

    courses = relationship("Course", back_populates="owner")
    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="student", cascade="all, delete-orphan")
    exam_submissions = relationship("ExamSubmission", back_populates="estudiante", cascade="all, delete-orphan")
    announcements = relationship("Announcement", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    student_profile = relationship("StudentProfile", back_populates="student", uselist=False)
    
    # Relación con Recomendaciones (un estudiante puede tener muchas recomendaciones)
    recomendaciones = relationship("RecomendacionEstudiante", back_populates="estudiante", cascade="all, delete-orphan")
    
    # Relación con Interacciones de Recursos (un estudiante puede tener muchas interacciones)
    interacciones_recursos = relationship("InteraccionRecurso", back_populates="estudiante", cascade="all, delete-orphan")