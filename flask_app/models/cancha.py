from flask_app.config.mysqlconnection import connectToMySQL
DATABASE = 'nosfalta1'

class Cancha:
    def __init__(self, data):
        self.id_cancha = data['id_cancha']
        self.nombre = data['nombre']
        self.id_recinto = data.get('id_recinto', None)  # Usar .get para evitar KeyError
        self.fecha_creacion = data['fecha_creacion']
        self.fecha_actualizacion = data['fecha_actualizacion']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM canchas;"
        resultados = connectToMySQL(DATABASE).query_db(query)
        canchas = []
        for cancha in resultados:
            canchas.append(cls(cancha))
        return canchas
    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO canchas (nombre, id_recinto, fecha_creacion, fecha_actualizacion)
        VALUES (%(nombre)s, %(id_recinto)s, NOW(), NOW());
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    @classmethod
    def get_by_recinto(cls, id_recinto):
        query = "SELECT * FROM canchas WHERE id_recinto = %(id_recinto)s;"
        data = {'id_recinto': id_recinto}
        resultados = connectToMySQL(DATABASE).query_db(query, data)
        canchas = []
        for cancha in resultados:
            canchas.append(cls(cancha))
        return canchas