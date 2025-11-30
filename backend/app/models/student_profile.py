# backend/app/models/student_profile.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class StudentProfile(Base):
    """
    Modelo para almacenar el cuestionario de perfil del estudiante.
    Estas variables se usan como features predictivas para el modelo ML.
    """
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column("estudiante_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    
    # Variables del cuestionario (escala 1-10)
    motivacion = Column("motivacion", Float, nullable=False, comment="Nivel de motivación (1-10)")
    tiempo_disponible = Column("tiempo_disponible", Float, nullable=False, comment="Tiempo disponible para estudiar (1-10)")
    horas_sueno = Column("horas_sueno", Float, nullable=False, comment="Horas de sueño por noche (1-10)")
    horas_estudio = Column("horas_estudio", Float, nullable=False, comment="Horas dedicadas a estudiar (1-10)")
    disfrute_estudio = Column("disfrute_estudio", Float, nullable=False, comment="Qué tanto le gusta estudiar (1-10)")
    tranquilidad_lugar_estudio = Column("tranquilidad_lugar_estudio", Float, nullable=False, comment="Tranquilidad del lugar de estudio (1-10)")
    presion_academica = Column("presion_academica", Float, nullable=False, comment="Presión académica percibida (1-10)")
    
    # Variable categórica
    genero = Column("genero", String(20), nullable=True, comment="Género del estudiante")
    
    # Timestamps
    fecha_creacion = Column("fecha_creacion", DateTime(timezone=True), server_default=func.now(), nullable=False)
    fecha_actualizacion = Column("fecha_actualizacion", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relación con User
    student = relationship("User", back_populates="student_profile", foreign_keys=[estudiante_id])

