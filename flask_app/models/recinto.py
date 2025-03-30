import logging
from flask_app.config.dbconnection import connectToPostgreSQL
from flask import flash
import re
import os

from dotenv import load_dotenv
env_file = os.getenv('ENV_FILE', '.env')  # Por defecto, carga .env
load_dotenv(dotenv_path=env_file)

# Asegurarse de que las variables de entorno estén configuradas
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DATABASE')

class Recinto:
    def __init__(self, data):
        self.id_recinto = data['id_recinto']
        self.nombre = data['nombre']
        self.direccion = data['direccion']
        self.id_localidad = data['id_localidad']
        self.localidad = data['localidad'] if 'localidad' in data else None
        self.provincia = data['provincia'] if 'provincia' in data else None
        self.pais = data['pais'] if 'pais' in data else None
        self.descripcion = data['descripcion'] if 'descripcion' in data else None
        self.imagen = data['imagen'] if 'imagen' in data else None
        self.fecha_creacion = data['fecha_creacion'] if 'fecha_creacion' in data else None
        self.fecha_modificacion = data['fecha_modificacion'] if 'fecha_modificacion' in data else None


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recintos;"
        resultados = connectToPostgreSQL(DATABASE).query_db(query)
        if not resultados:  # Si no hay resultados, devuelve una lista vacía
            return []
        logging.info(f"Resultados de la consulta: {resultados}")
        recintos  = []
        for recinto in resultados:
            recintos.append(cls(recinto))
        return recintos

    @classmethod
    def registrar_recinto(cls, data):
        query = """
        INSERT INTO recintos (nombre, direccion, id_localidad) 
        VALUES (%(nombre)s, %(direccion)s, %(id_localidad)s) RETURNING id_recinto;
        """
        logging.info(f"Datos enviados para guardar recinto: {data}")
        try:
            resultado = connectToPostgreSQL(DATABASE).query_db(query, data)
            logging.info(f"Resultado de la consulta: {resultado}")
            return resultado
        except Exception as e:
            logging.error(f"Error al guardar recinto: {e}")
            return None


