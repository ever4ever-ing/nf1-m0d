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
        self.id_recinto = data.get('id_recinto')  # Usa get para evitar KeyError
        self.nombre = data['nombre']
        self.direccion = data['direccion']
        self.id_localidad = data['id_localidad']
        self.localidad = data.get('localidad')  # Usa get para evitar KeyError
        self.descripcion = data.get('descripcion')
        self.imagen = data.get('imagen')
        self.fecha_creacion = data.get('fecha_creacion')
        self.fecha_modificacion = data.get('fecha_modificacion')

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recintos;"
        resultados = connectToPostgreSQL(DATABASE).query_db(query)
        if not resultados:  # Si no hay resultados, devuelve una lista vacía
            return []
        logging.info(f"Resultados de la consulta: {resultados}")
        recintos = []
        for recinto in resultados:
            if isinstance(recinto, dict):  # Asegúrate de que cada elemento sea un diccionario
                recintos.append(cls(recinto))
            else:
                logging.error(f"Elemento inválido en resultados: {recinto}")
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
        
    @classmethod
    def obtener_por_id(cls, id_recinto):
        query = "SELECT * FROM recintos WHERE id_recinto = %s;"
        data = (id_recinto,)
        resultado = connectToPostgreSQL(DATABASE).query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None

    @classmethod
    def obtener_por_id_localidad(cls, id_localidad):
        query = "SELECT * FROM recintos WHERE id_localidad = %s;"
        data = (id_localidad,)
        resultado = connectToPostgreSQL(DATABASE).query_db(query, data)
        logging.info(f"Resultado de la consulta: {resultado}")
        logging.info(f"type resultado: {type(resultado)}")
        if resultado:
            recintos = []
            for recinto in resultado:
                recintos.append(cls(recinto))  # Crear un objeto Recinto por cada resultado
            return recintos  # Devolver una lista de objetos Recinto
        return []


