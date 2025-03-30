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
    telefono VARCHAR(20),
    fecha_nacimiento DATE,
    fecha_ultimo_acceso TIMESTAMP,
    fecha_ultimo_login TIMESTAMP,
    fecha_ultimo_logout TIMESTAMP,
    fecha_ultimo_cambio_password TIMESTAMP,
    fecha_ultimo_cambio_email TIMESTAMP,
    fecha_ultimo_cambio_telefono TIMESTAMP,
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
    id_localidad INT NOT NULL,
    id_recinto INT NOT NULL,
    id_cancha INT NOT NULL,
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

-- Tabla de localidades
CREATE TABLE localidades (
    id_localidad SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Insertar todas las localidades de Chile
INSERT INTO localidades (nombre) VALUES 
('Arica'),
('Iquique'),
('Antofagasta'),
('Copiapó'),
('La Serena'),
('Valparaíso'),
('Santiago'),
('Rancagua'),
('Talca'),
('Chillán'),
('Concepción'),
('Temuco'),
('Valdivia'),
('Puerto Montt'),
('Coyhaique'),
('Punta Arenas'),
('Calama'),
('Quillota'),
('San Antonio'),
('Melipilla'),
('Curicó'),
('Los Ángeles'),
('Osorno'),
('Puerto Varas'),
('Castro'),
('Ancud'),
('Vallenar'),
('Ovalle'),
('San Fernando'),
('Linares'),
('Coronel'),
('Talcahuano'),
('Lota'),
('Angol'),
('Villarrica'),
('Pucón'),
('La Unión'),
('Río Bueno'),
('Quellón'),
('Aysén'),
('Porvenir'),
('Natales');

-- Crear un trigger para actualizar fecha_actualizacion en la tabla localidades
CREATE TRIGGER trigger_update_localidades
BEFORE UPDATE ON localidades
FOR EACH ROW
EXECUTE FUNCTION update_fecha_actualizacion();

-- Tabla de recintos
CREATE TABLE recintos (
    id_recinto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion TEXT NOT NULL,
    id_localidad INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_localidad) REFERENCES localidades(id_localidad)
);

-- Crear un trigger para actualizar fecha_actualizacion en la tabla recintos
CREATE TRIGGER trigger_update_recintos
BEFORE UPDATE ON recintos
FOR EACH ROW
EXECUTE FUNCTION update_fecha_actualizacion();

-- Tabla de canchas
CREATE TABLE canchas (
    id_cancha SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_recinto INT NOT NULL,
    tipo VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_recinto) REFERENCES recintos(id_recinto)
);

-- Crear un trigger para actualizar fecha_actualizacion en la tabla canchas
CREATE TRIGGER trigger_update_canchas
BEFORE UPDATE ON canchas
FOR EACH ROW
EXECUTE FUNCTION update_fecha_actualizacion();

-- Tabla de reservas de hora
CREATE TABLE reservas (
    id_reserva SERIAL PRIMARY KEY,
    id_cancha INT NOT NULL,
    id_usuario INT NOT NULL,
    fecha_reserva TIMESTAMP NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cancha) REFERENCES canchas(id_cancha),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- Crear un trigger para actualizar fecha_actualizacion en la tabla reservas
CREATE TRIGGER trigger_update_reservas
BEFORE UPDATE ON reservas
FOR EACH ROW
EXECUTE FUNCTION update_fecha_actualizacion();