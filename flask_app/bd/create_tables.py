import psycopg2
import logging

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URL de conexión
DB_URL = "postgresql://root:eEiZH4x3WKKgGm2bCGlWgA5iAia3o9dH@dpg-cve7hu52ng1s73ce43pg-a.oregon-postgres.render.com/nf1_iv1y"

# Script SQL para crear las tablas
CREATE_TABLES_SQL = """
-- Crear la tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear la función y trigger para actualizar fecha_actualizacion en usuarios
CREATE OR REPLACE FUNCTION update_fecha_actualizacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER IF NOT EXISTS trigger_update_usuarios
BEFORE UPDATE ON usuarios
FOR EACH ROW
EXECUTE FUNCTION update_fecha_actualizacion();

-- Crear la tabla de partidos
CREATE TABLE IF NOT EXISTS partidos (
    id_partido SERIAL PRIMARY KEY,
    lugar VARCHAR(100) NOT NULL,
    fecha_inicio TIMESTAMP NOT NULL,
    descripcion TEXT,
    id_organizador INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_organizador) REFERENCES usuarios(id_usuario)
);

-- Crear el trigger para actualizar fecha_actualizacion en partidos
CREATE TRIGGER IF NOT EXISTS trigger_update_partidos
BEFORE UPDATE ON partidos
FOR EACH ROW
EXECUTE FUNCTION update_fecha_actualizacion();

-- Crear la tabla de participantes
CREATE TABLE IF NOT EXISTS participantes_partido (
    id_participante SERIAL PRIMARY KEY,
    id_partido INT NOT NULL,
    id_usuario INT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_partido) REFERENCES partidos(id_partido),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);
"""

def create_tables():
    try:
        logging.info("Conectando a la base de datos...")
        connection = psycopg2.connect(DB_URL)
        cursor = connection.cursor()
        logging.info("Creando tablas...")
        cursor.execute(CREATE_TABLES_SQL)
        connection.commit()
        logging.info("Tablas creadas exitosamente.")
    except Exception as e:
        logging.error(f"Error al crear las tablas: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            logging.info("Conexión cerrada.")

if __name__ == "__main__":
    create_tables()
