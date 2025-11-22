from flask_app.config.mysqlconnection import connectToMySQL, DB_HOST, DB_USER, DB_PASSWORD, DATABASE
import logging
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE = os.getenv('MYSQL_DATABASE')
class Participante:
    def __init__(self, data):
        self.id_participante = data['id_participante']
        self.id_partido = data['id_partido']
        self.id_usuario = data['id_usuario']

    @classmethod
    def agregar_participante(cls, data):
        query = """
            INSERT INTO participantes_partido(id_partido, id_usuario)
            VALUES (%(id_partido)s, %(id_usuario)s);
        """
        logging.debug("Agregando participante:")
        logging.debug(query)
        return connectToMySQL(DATABASE).query_db(query, data)
    @classmethod
    def eliminar_participante(cls, data):
        query = """
            DELETE FROM participantes_partido WHERE id_usuario = %(id_usuario)s and id_partido = %(id_partido)s;
        """
        logging.debug("Eliminando participante:")
        logging.debug(query)
        return connectToMySQL(DATABASE).query_db(query, data)
    @classmethod
    def verificar_participante(cls, id_partido, id_usuario):
        query = """
            SELECT * FROM participantes_partido 
            WHERE id_partido = %(id_partido)s AND id_usuario = %(id_usuario)s;
        """
        data = {
            'id_partido': id_partido,
            'id_usuario': id_usuario
        }
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result != None

    @classmethod
    def obtener_participantes_por_partido(cls, id_partido):
        query = """
            SELECT p.*, u.nombre 
            FROM participantes_partido p
            JOIN usuarios u ON p.id_usuario = u.id_usuario
            WHERE p.id_partido = %(id_partido)s;
        """
        data = {'id_partido': id_partido}
        results = connectToMySQL(DATABASE).query_db(query, data)
        logging.debug(type(results))
        participantes = []
        if results:
            for row in results:
                logging.debug(row)
                participantes.append(row)
        
        #for participante in participantes:
            # Acceder a los atributos de cada participante
        #    logging.e(f"Datos del participante: {participante}")

        return participantes

