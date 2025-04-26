from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import participante
import os

from dotenv import load_dotenv
env_file = os.getenv('ENV_FILE', '.env')  # Por defecto, carga .env
load_dotenv(dotenv_path=env_file)

# Asegurarse de que las variables de entorno estén configuradas
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DATABASE')

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
            SELECT * FROM localidades WHERE id_localidad = %s
        """
        data = (id_localidad,)
        resultado = connectToPostgreSQL(DATABASE).query_db(query, data)
        if resultado:
            return cls(resultado[0])
        else:
            return None