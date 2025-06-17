import logging
from flask_app.models import participante
import os
from flask_app.config.mysqlconnection import connectToMySQL, DB_HOST, DB_USER, DB_PASSWORD, DATABASE


log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO))

class Localidad:
    def __init__(self, data):
        self.id_localidad = data['id_localidad']
        self.nombre = data['nombre']

    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM localidades
        """
        resultado = connectToMySQL(DATABASE).query_db(query)
        localidades = []
        if resultado:
            for localidad in resultado:
                localidades.append(cls(localidad))
        else:
            print("No se encontraron localidades.")

        return localidades
    
    @classmethod
    def obtener_por_id(cls, id_localidad):
        query = """
            SELECT * FROM localidades WHERE id_localidad = %(id_localidad)s
        """
        data = {'id_localidad': id_localidad}  # Cambiar a un diccionario para evitar errores
        resultado = connectToMySQL(DATABASE).query_db(query, data)
        if resultado:
            logging.debug(f"Resultado de la consulta en obtener localidad por id: {resultado}")
            return cls(resultado[0])
        else:

            logging.error(f"No se encontró localidad con id {id_localidad}.")
            return None