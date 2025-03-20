from flask_app.config.dbconnection import connectToPostgreSQL
import os
DATABASE =os.getenv('DATABASE', 'nosfalta1')

class Participante:
    def __init__(self, data):
        self.id_participante = data['id_participante']
        self.id_partido = data['id_partido']
        self.id_usuario = data['id_usuario']

    @classmethod
    def agregar_participante(cls, data):
        query = """
            INSERT INTO participantes_partido (id_partido, id_usuario)
            VALUES (%(id_partido)s, %(id_usuario)s)
            RETURNING id_participante;
        """
        print("Agregando participante:")
        print(query)
        resultado = connectToPostgreSQL(DATABASE).query_db(query, data)
        if resultado:
            return resultado[0]['id_participante']  # Devuelve el ID del participante generado
        return None

    @classmethod
    def eliminar_participante(cls, data):
        query = """
            DELETE FROM participantes_partido 
            WHERE id_usuario = %(id_usuario)s AND id_partido = %(id_partido)s;
        """
        print("Eliminando participante:")
        print(query)
        return connectToPostgreSQL(DATABASE).query_db(query, data)

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
        result = connectToPostgreSQL(DATABASE).query_db(query, data)
        return bool(result)  # Devuelve True si hay resultados, False si no

    @classmethod
    def obtener_participantes_por_partido(cls, id_partido):
        query = """
            SELECT p.*, u.nombre 
            FROM participantes_partido p
            JOIN usuarios u ON p.id_usuario = u.id_usuario
            WHERE p.id_partido = %(id_partido)s;
        """
        data = {'id_partido': id_partido}
        results = connectToPostgreSQL(DATABASE).query_db(query, data)
        print(type(results))
        participantes = []
        if results:
            for row in results:
                print(row)
                participantes.append(row)
        
        for participante in participantes:
            # Acceder a los atributos de cada participante
            print("Datos del participante:", participante)

        return participantes