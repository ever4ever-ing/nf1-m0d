# Instrucciones para aplicar la migración de notificaciones

## Paso 1: Conectarse a MySQL

```bash
mysql -u root -p
```

## Paso 2: Seleccionar la base de datos

```sql
USE nf1;
```

## Paso 3: Ejecutar el script SQL

```sql
-- Tabla de notificaciones
CREATE TABLE IF NOT EXISTS notificaciones (
    id_notificacion INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    mensaje TEXT NOT NULL,
    id_partido INT,
    leida BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_partido) REFERENCES partidos(id_partido) ON DELETE CASCADE,
    INDEX idx_usuario_leida (id_usuario, leida),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## Alternativa: Ejecutar desde terminal

```bash
mysql -u root -p nf1 < flask_app/bd/notificaciones.sql
```

## Verificar que la tabla se creó correctamente

```sql
DESCRIBE notificaciones;
SELECT * FROM notificaciones;
```
