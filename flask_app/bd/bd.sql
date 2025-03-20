CREATE DATABASE nosfalta1;
\c nosfalta1;

-- Tabla de usuarios
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de partidos
CREATE TABLE partidos (
    id_partido SERIAL PRIMARY KEY,
    lugar VARCHAR(100) NOT NULL,
    fecha_inicio TIMESTAMP NOT NULL,
    descripcion TEXT,
    id_organizador INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_organizador FOREIGN KEY (id_organizador) REFERENCES usuarios(id_usuario)
);

-- Tabla de participantes
CREATE TABLE participantes_partido (
    id_participante SERIAL PRIMARY KEY,
    id_partido INT NOT NULL,
    id_usuario INT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_partido FOREIGN KEY (id_partido) REFERENCES partidos(id_partido),
    CONSTRAINT fk_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);