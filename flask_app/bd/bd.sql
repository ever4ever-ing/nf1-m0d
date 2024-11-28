CREATE DATABASE IF NOT EXISTS nosfalta1;
USE nosfalta1;

-- Tabla de usuarios
CREATE TABLE usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de partidos
CREATE TABLE partidos (
    id_partido INT PRIMARY KEY AUTO_INCREMENT,
    lugar VARCHAR(100) NOT NULL,
    fecha_inicio DATE NOT NULL,
    descripcion TEXT,
    id_organizador INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_organizador) REFERENCES usuarios(id_usuario)
);

-- Tabla de participantes
CREATE TABLE participantes_partido (
    id_participante INT PRIMARY KEY AUTO_INCREMENT,
    id_partido INT NOT NULL,
    id_usuario INT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_partido) REFERENCES partido(id),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);