# backend/app/models/course.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.db.base import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column("titulo", String, index=True, nullable=False)
    descripcion = Column("descripcion", String, nullable=True)
    
    fecha_creacion = Column("fecha_creacion", DateTime(timezone=True), server_default=text("NOW()"), nullable=False)
    
    propietario_id = Column("propietario_id", Integer, ForeignKey("users.id"), nullable=False)

    # --- Relaciones ---
    owner = relationship("User", back_populates="courses", foreign_keys=[propietario_id])
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    
    # --- ASEGÚRATE DE QUE ESTA LÍNEA ESTÉ ASÍ ---
    tasks = relationship("Task", back_populates="course", cascade="all, delete-orphan")
    announcements = relationship("Announcement", back_populates="course", cascade="all, delete-orphan")