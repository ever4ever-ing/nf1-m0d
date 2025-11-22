-- Migración: Permitir NULL en fecha_inicio de la tabla partidos
-- Fecha: 22 de noviembre de 2025
-- Descripción: Modifica la columna fecha_inicio para permitir valores NULL

USE nf1;

-- Modificar la columna fecha_inicio para permitir NULL
ALTER TABLE partidos 
MODIFY COLUMN fecha_inicio DATETIME NULL;

-- Verificar el cambio
DESCRIBE partidos;

-- Nota: Esta migración es segura y no afectará los datos existentes
