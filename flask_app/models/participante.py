from flask_app.config.mysqlconnection import connectToMySQL

DATABASE = 'nosfalta1'

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
        print("Agregando participante:")
        print(query)
        return connectToMySQL(DATABASE).query_db(query, data)
    @classmethod
    def eliminar_participante(cls, data):
        query = """
            DELETE FROM participantes_partido WHERE id_usuario = %(id_usuario)s and id_partido = %(id_partido)s;
        """
        print("Eliminando participante:")
        print(query)
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

