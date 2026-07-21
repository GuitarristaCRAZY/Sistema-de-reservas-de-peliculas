from datetime import datetime
from database import SessionLocal, engine, Base
import models
from crud import (
    registrar_usuario, 
    autenticar_usuario, 
    crear_pelicula, 
    crear_horario, 
    obtener_horarios, 
    crear_reserva, 
    obtener_reservas_usuario,
    eliminar_pelicula
)

Base.metadata.create_all(bind=engine)

def menu_principal():
    db = SessionLocal()
    
    if not db.query(models.Usuario).filter(models.Usuario.nombre_usuario == "admin").first():
        registrar_usuario(db, "admin", "admin@cine.com", "1234", rol="admin")
        print("👤 Usuario 'admin' creado (Contraseña: 1234)")
        
        p1 = crear_pelicula(db, "The Batman", "SuperHeroe", "Accion", "poster_estreno.jpg")
        crear_horario(db, p1.id, datetime(2026, 7, 30, 20, 0), "Sala VIP 1", 30)
        
        p2 = crear_pelicula(db, "Spider-Man: No Way Home", "Multiverso", "Ciencia Ficcion", "spiderman.jpg")
        crear_horario(db, p2.id, datetime(2026, 8, 1, 18, 0), "Sala 2", 40)
        crear_horario(db, p2.id, datetime(2026, 8, 2, 22, 0), "Sala 3", 35)

        p3 = crear_pelicula(db, "Interestelar", "Viaje en el espacio", "Ciencia Ficcion", "interestelar.jpg")
        crear_horario(db, p3.id, datetime(2026, 7, 31, 21, 30), "Sala IMAX", 50)

    if not db.query(models.Usuario).filter(models.Usuario.nombre_usuario == "usuario").first():
        registrar_usuario(db, "usuario", "usuario@cine.com", "1234", rol="usuario")
        print("👤 Usuario 'usuario' creado (Contrasena: 1234)")

    usuario_actual = None

    while True:
        print("\n========================================")
        print("          🎬 CINE CRAZY - SISTEMA       ")
        print("========================================")
        
        if not usuario_actual:
            print("1. Iniciar Sesion")
            print("2. Salir")
            opcion = input("\nElige una opcion: ").strip()

            if opcion == "1":
                username = input("Usuario: ").strip()
                password = input("Contrasena: ").strip()
                user = autenticar_usuario(db, username, password)
                if user:
                    usuario_actual = user
                    print(f"\n¡Bienvenido, {user.nombre_usuario}! [Rol: {user.rol.upper()}]")
                else:
                    print("\n❌ Usuario o contraseña incorrectos.")
            
            elif opcion == "2":
                print("\n¡Gracias por usar Cine Crazy!")
                break
            else:
                print("\nOpcion invalida.")
        else:
            print(f"\nConectado como: {usuario_actual.nombre_usuario} [{usuario_actual.rol.upper()}]")
            print("1. Ver Cartelera y Horarios")
            print("2. Hacer una Reserva (Cliente)")
            print("3. Ver Mis Reservas")
            
            if usuario_actual.rol == "admin":
                print("4. [ADMIN] Agregar Pelicula")
                print("5. [ADMIN] Crear Horario")
                print("6. [ADMIN] Eliminar Pelicula")
            
            print("0. Cerrar Sesion")
            
            opcion = input("\nElige una opcion: ").strip()

            if opcion == "1":
                print("\n--- CARTELERA DE PELICULAS Y FUNCIONES ---")
                horarios = obtener_horarios(db)
                if not horarios:
                    print("No hay funciones programadas.")
                for h in horarios:
                    print(f"\n[ID Funcion: {h.id}] Pelicula: {h.pelicula.titulo}")
                    print(f"  Genero: {h.pelicula.genero} | Sinopsis: {h.pelicula.descripcion}")
                    print(f"  🖼️ Imagen / Poster: {h.pelicula.imagen_url}")
                    print(f"  📅 Fecha/Hora: {h.fecha_hora} | 📍 Sala: {h.sala} | 🎟️ Asientos libres: {h.asientos_disponibles}")

            elif opcion == "2":
                print("\n--- RESERVAR ASIENTOS ---")
                horarios = obtener_horarios(db)
                if not horarios:
                    print("No hay funciones disponibles para reservar.")
                    continue
                
                for h in horarios:
                    print(f"ID: {h.id} | {h.pelicula.titulo} - {h.fecha_hora} ({h.sala}) - Libres: {h.asientos_disponibles}")
                
                try:
                    h_id = int(input("\nIngresa el ID de la funcion que deseas: ").strip())
                    cant = int(input("¿Cuantos asientos deseas reservar?: ").strip())
                    
                    reserva = crear_reserva(db, usuario_id=usuario_actual.id, horario_id=h_id, cantidad_asientos=cant)
                    print(f"\n🎉 ¡Reserva realizada con exito! ID de tu ticket: {reserva.id}")
                except ValueError as e:
                    print(f"\n❌ Error en la reserva: {e}")

            elif opcion == "3":
                print("\n--- TUS RESERVAS ---")
                mis_res = obtener_reservas_usuario(db, usuario_id=usuario_actual.id)
                if not mis_res:
                    print("No tienes reservas registradas.")
                for r in mis_res:
                    print(f"- Reserva #{r.id} | Pelicula: {r.horario.pelicula.titulo} | Funcion: {r.horario.fecha_hora} | Asientos: {r.cantidad_asientos}")

            elif opcion == "4" and usuario_actual.rol == "admin":
                print("\n--- [ADMIN] AGREGAR NUEVA PELICULA ---")
                titulo = input("Titulo: ").strip()
                desc = input("Descripcion: ").strip()
                genero = input("Genero: ").strip()
                img = input("Nombre o archivo de la imagen (ej: batman.jpg): ").strip()
                crear_pelicula(db, titulo, desc, genero, img)
                print("\n✨ ¡Pelicula agregada a la cartelera con exito!")

            elif opcion == "5" and usuario_actual.rol == "admin":
                print("\n--- [ADMIN] PROGRAMAR NUEVO HORARIO ---")
                peliculas = db.query(models.Pelicula).all()
                for p in peliculas:
                    print(f"ID: {p.id} - {p.titulo}")
                try:
                    p_id = int(input("ID de la pelicula: ").strip())
                    sala = input("Nombre de la sala (ej: Sala 2): ").strip()
                    asientos = int(input("Capacidad de asientos: ").strip())
                    print("Ingresa la fecha y hora de la funcion:")
                    anio = int(input("Año (ej: 2026): "))
                    mes = int(input("Mes (1-12): "))
                    dia = int(input("Dia (1-31): "))
                    hora = int(input("Hora en formato 24h (ej: 18): "))
                    minuto = int(input("Minutos (ej: 0): "))
                    f_hora = datetime(anio, mes, dia, hora, minuto)
                    crear_horario(db, p_id, f_hora, sala, asientos)
                    print("\n✨ ¡Horario creado con exito!")
                except Exception as e:
                    print(f"\n❌ Error al crear horario: {e}")
            
            elif opcion == "6" and usuario_actual.rol == "admin":
                print("\n--- [ADMIN] ELIMINAR PELICULA ---")
                peliculas = db.query(models.Pelicula).all()
                if not peliculas:
                    print("No hay peliculas registradas.")
                else:
                    for p in peliculas:
                        print(f"ID: {p.id} - {p.titulo}")
                    try:
                        p_id = int(input("\nIngresa el ID de la pelicula que deseas eliminar: ").strip())
                        eliminar_pelicula(db, p_id)
                        print("\n🗑️ ¡Pelicula eliminada con exito de la cartelera!")
                    except ValueError as e:
                        print(f"\n❌ Error al eliminar: {e}")

            elif opcion == "0":
                usuario_actual = None
                print("\nSesion cerrada.")
            else:
                print("\nOpcion invalida.")

    db.close()

if __name__ == "__main__":
    menu_principal()

