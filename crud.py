from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from models import Usuario
from datetime import datetime
from models import Horario
from models import Pelicula


def eliminar_pelicula(db: Session, pelicula_id: int):
    pelicula = db.query(Pelicula).filter(Pelicula.id == pelicula_id).first()
    if not pelicula:
        raise ValueError("La película no existe.")
    
    db.delete(pelicula)
    db.commit()
    return True

def obtener_password_hash(password: str) -> str:
    return generate_password_hash(password)

def verificar_password(password_plana: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, password_plana)

def registrar_usuario(db: Session, nombre_usuario: str, correo: str, password: str, rol: str = "usuario"):
    password_hash = obtener_password_hash(password)
    nuevo_usuario = Usuario(
        nombre_usuario=nombre_usuario,
        correo=correo,
        contrasena_hash=password_hash,
        rol=rol
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def autenticar_usuario(db: Session, nombre_usuario: str, password: str):
    usuario = db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()
    if not usuario:
        return None
    if not verificar_password(password, usuario.contrasena_hash):
        return None
    return usuario

def crear_horario(db: Session, pelicula_id: int, fecha_hora: datetime, sala: str, asientos: int = 50):
    nuevo_horario = Horario(
        pelicula_id=pelicula_id,
        fecha_hora=fecha_hora,
        sala=sala,
        asientos_disponibles=asientos
    )
    db.add(nuevo_horario)
    db.commit()
    db.refresh(nuevo_horario)
    return nuevo_horario

def obtener_horarios(db: Session):
    return db.query(Horario).all()

from models import Reserva, Horario

def crear_reserva(db: Session, usuario_id: int, horario_id: int, cantidad_asientos: int):
  
    horario = db.query(Horario).filter(Horario.id == horario_id).first()
    
    if not horario:
        raise ValueError("El horario seleccionado no existe.")
    
    if horario.asientos_disponibles < cantidad_asientos:
        raise ValueError(f"No hay suficientes asientos disponibles. Solo quedan {horario.asientos_disponibles}.")
    
    
    nueva_reserva = Reserva(
        usuario_id=usuario_id,
        horario_id=horario_id,
        cantidad_asientos=cantidad_asientos
    )
    
    
    horario.asientos_disponibles -= cantidad_asientos
    
    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)
    db.refresh(horario)
    
    return nueva_reserva

def obtener_reservas_usuario(db: Session, usuario_id: int):
    return db.query(Reserva).filter(Reserva.usuario_id == usuario_id).all()

def crear_pelicula(db: Session, titulo: str, descripcion: str, genero: str, imagen_url: str = None):
    nueva_pelicula = Pelicula(
        titulo=titulo,
        descripcion=descripcion,
        genero=genero,
        imagen_url=imagen_url
    )
    db.add(nueva_pelicula)
    db.commit()
    db.refresh(nueva_pelicula)
    return nueva_pelicula