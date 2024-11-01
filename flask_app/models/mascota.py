from flask_app.config.mysqlconnection import connectToMySQL


class Mascota:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.tipo = data['tipo']
        self.color = data['color']
        self.usuario_id = data['usuario_id']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM mascotas;"
        resultados = connectToMySQL('pet').query_db(query)
        mascotas = []
        for mascota in resultados:
            mascotas.append(cls(mascota))
        return mascotas

    @classmethod
    def save(cls, datos):
        query = """
        INSERT INTO mascotas (nombre, tipo, color, usuario_id) 
        VALUES (%(nombre)s, %(tipo)s, %(color)s, %(usuario_id)s);
        """
        return connectToMySQL('pet').query_db(query, datos)

    @classmethod
    def get_by_usuario(cls, usuario_id):
        query = "SELECT * FROM mascotas WHERE usuario_id = %(usuario_id)s;"
        resultados = connectToMySQL('pet').query_db(
            query, {'usuario_id': usuario_id})
        mascotas = []
        for mascota in resultados:
            mascotas.append(cls(mascota))
        return mascotas

    @classmethod
    def get_by_id(cls, mascota_id):
        query = "SELECT * FROM mascotas WHERE id = %(id)s;"
        resultado = connectToMySQL('pet').query_db(query, {'id': mascota_id})
        if resultado:
            return cls(resultado[0])
        return None

    @classmethod
    def update(cls, datos):
        query = """
        UPDATE mascotas 
        SET nombre = %(nombre)s, tipo = %(tipo)s, color = %(color)s 
        WHERE id = %(id)s;
        """
        return connectToMySQL('pet').query_db(query, datos)

    @classmethod
    def delete(cls, mascota_id):
        query = "DELETE FROM mascotas WHERE id = %(id)s;"
        return connectToMySQL('pet').query_db(query, {'id': mascota_id})

    @staticmethod
    def validar_mascota(datos):
        es_valido = True
        if len(datos['nombre']) < 3:
            print("Nombre muy corto")
            es_valido = False
        if len(datos['tipo']) < 3:
            es_valido = False
        if len(datos['color']) < 3:
            es_valido = False
        return es_valido
