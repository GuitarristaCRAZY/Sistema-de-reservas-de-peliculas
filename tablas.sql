#Usuario
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    es_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE peliculas (
    id SERIAL PRIMARY KEY, 
    titulo VARCHAR(150),
    descripcion TEXT, 
    poster_URL VARCHAR(255),
    genero BOOLEAN VARCHAR(50)
);

CREATE TABLE asientos (
    id SERIAL PRIMARY KEY,
    sala_id INTEGER REFERENCES salas(id),
    numero_asientos INTEGER
);

CREATE TABLE horarios (
    id SERIAL PRIMARY KEY,
    pelicula_id INTEGER REFERENCES peliculas(id),
    sala_id INTEGER REFERENCES salas (id),
    fecha_hora TIMESTAMP

);

CREATE TABLE reservas (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    horario_id INTEGER REFERENCES horarios(id),
    fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE detalle_reservas (
    reserva_id INTEGER REFERENCES reservas(id),
    asiento_id INTEGER REFERENCES asientos(id),
    PRIMARY KEY (reserva_id, asiento_id)
);