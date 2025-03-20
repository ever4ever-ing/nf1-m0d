-- Crear la base de datos (si no existe)
CREATE DATABASE nosfalta1;

-- Conectarse a la base de datos (esto se hace fuera del script, en la conexión de la aplicación o herramienta)

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

-- Crear un trigger para actualizar fecha_actualizacion en la tabla usuarios
CREATE OR REPLACE FUNCTION update_fecha_actualizacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_usuarios
BEFORE UPDATE ON usuarios
FOR EACH ROW
EXECUTE FUNCTION update_fecha_actualizacion();

-- Tabla de partidos
CREATE TABLE partidos (
    id_partido SERIAL PRIMARY KEY,
    lugar VARCHAR(100) NOT NULL,
    fecha_inicio TIMESTAMP NOT NULL,
    descripcion TEXT,
    id_organizador INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_organizador) REFERENCES usuarios(id_usuario)
);

-- Crear un trigger para actualizar fecha_actualizacion en la tabla partidos
CREATE TRIGGER trigger_update_partidos
BEFORE UPDATE ON partidos
FOR EACH ROW
EXECUTE FUNCTION update_fecha_actualizacion();

-- Tabla de participantes
CREATE TABLE participantes_partido (
    id_participante SERIAL PRIMARY KEY,
    id_partido INT NOT NULL,
    id_usuario INT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_partido) REFERENCES partidos(id_partido),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);