# backend/app/models/comment.py
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.db.base import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    contenido = Column("contenido", Text, nullable=False)
    
    fecha_creacion = Column("fecha_creacion", DateTime(timezone=True), server_default=text("NOW()"), nullable=False)
    
    # Claves foráneas
    anuncio_id = Column("anuncio_id", Integer, ForeignKey("announcements.id"), nullable=False)
    autor_id = Column("autor_id", Integer, ForeignKey("users.id"), nullable=False)

    # --- Relaciones ---
    announcement = relationship("Announcement", back_populates="comments", foreign_keys=[anuncio_id])
    author = relationship("User", back_populates="comments", foreign_keys=[autor_id])

    def __repr__(self):
        return f"<Comment(id={self.id}, anuncio_id={self.anuncio_id}, autor_id={self.autor_id})>"


