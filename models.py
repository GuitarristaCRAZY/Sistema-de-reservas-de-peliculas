from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Pelicula(Base):
    __tablename__ = "peliculas"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(String)
    genero = Column(String(50))
    imagen_url = Column(String(255))
    horarios = relationship("Horario", back_populates="pelicula", cascade="all, delete-orphan")

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(50), unique=True, index=True, nullable=False)
    correo = Column(String(100), unique=True, index=True, nullable=False)
    contrasena_hash = Column(String(255), nullable=False)
    rol = Column(String(20), default="usuario", nullable=False)
    activo = Column(Boolean, default=True)

class Horario(Base):
    __tablename__ = "horarios"

    id = Column(Integer, primary_key=True, index=True)
    pelicula_id = Column(Integer, ForeignKey("peliculas.id"))
    fecha_hora = Column(DateTime, nullable=False)
    sala = Column(String(50), nullable=False)  
    asientos_disponibles = Column(Integer, default=50) 
    pelicula = relationship("Pelicula", back_populates="horarios")
    reservas = relationship("Reserva", back_populates="horario", cascade="all, delete-orphan")

class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    horario_id = Column(Integer, ForeignKey("horarios.id"), nullable=False)
    cantidad_asientos = Column(Integer, nullable=False)
    fecha_reserva = Column(DateTime, default=datetime.utcnow)

  
    usuario = relationship("Usuario")
    horario = relationship("Horario")