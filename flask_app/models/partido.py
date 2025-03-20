from flask_app.config.dbconnection import connectToPostgreSQL
from flask_app.models import participante

DATABASE = 'nosfalta1'


class Partido:
    def __init__(self, data):
        self.id_partido = data['id_partido']
        self.lugar = data['lugar']
        self.fecha_inicio = data['fecha_inicio']
        self.descripcion = data['descripcion']
        self.id_organizador = data['id_organizador']
        self.fecha_creacion = data['fecha_creacion']
        self.fecha_actualizacion = data['fecha_actualizacion']
        self.organizador = data.get('organizador', None)
        self.participantes = []

    @classmethod
    def get_all(cls):
        query = """
            SELECT v.*, u.nombre as organizador 
            FROM partidos v
            JOIN usuarios u ON v.id_organizador = u.id_usuario
            ORDER BY v.fecha_inicio;
        """
        resultado = connectToPostgreSQL(DATABASE).query_db(query)
        partidos = []
        if resultado:
            for partido in resultado:
                cls(partido).participantes = participante.Participante.obtener_participantes_por_partido(
                    partido['id_partido'])
                partidos.append(cls(partido))
        return partidos

    @classmethod
    def get_match_disponibles(cls, id_usuario):
        query = """
            SELECT p.*, u.nombre as organizador
            FROM partidos p
            JOIN usuarios u ON p.id_organizador = u.id_usuario
            WHERE p.id_organizador != %s
            ORDER BY p.fecha_inicio;
        """
        data = (id_usuario,)
        results = connectToPostgreSQL(DATABASE).query_db(query, data)
        partidos = []
        if results:
            for row in results:
                partidos.append(cls(row))
        return partidos

    @classmethod
    def obtener_por_id(cls, id_partido):
        query = """
            SELECT p.*, u.nombre as organizador
            FROM partidos p
            JOIN usuarios u ON p.id_organizador = u.id_usuario
            WHERE p.id_partido = %s;
        """
        data = (id_partido,)
        results = connectToPostgreSQL(DATABASE).query_db(query, data)
        return cls(results[0]) if results else None


    @classmethod
    def crear(cls, data):
        query = """
            INSERT INTO partidos (lugar, fecha_inicio, descripcion, id_organizador)
            VALUES (%(lugar)s, %(fecha_inicio)s, %(descripcion)s, %(id_organizador)s)
            RETURNING id_partido;
        """
        # Ejecutar la consulta y obtener el resultado
        resultado = connectToPostgreSQL(DATABASE).query_db(query, data)
        print("Resultado:", resultado)
        # Verificar si se obtuvo un resultado y devolver el id_partido
        if resultado:
            return resultado[0]['id_partido']  # Devuelve el id_partido generado
        return None  # Si no hay resultado, devuelve None

    @classmethod
    def actualizar(cls, data):
        query = """
            UPDATE partidos 
            SET lugar = %s,
                fecha_inicio = %s,
                descripcion = %s
            WHERE id_partido = %s;
        """
        data_tuple = (data['lugar'], data['fecha_inicio'],
                      data['descripcion'], data['id_partido'])
        return connectToPostgreSQL(DATABASE).query_db(query, data_tuple)

    @classmethod
    def eliminar(cls, id_partido):
        query1 = "DELETE FROM participantes_partido WHERE id_partido = %s;"
        query2 = "DELETE FROM partidos WHERE id_partido = %s;"
        data = (id_partido,)
        connectToPostgreSQL(DATABASE).query_db(query1, data)
        connectToPostgreSQL(DATABASE).query_db(query2, data)
        return True

    @classmethod
    def obtener_por_organizador(cls, id_organizador):
        query = """
            SELECT v.*, u.nombre as organizador 
            FROM partidos v
            JOIN usuarios u ON v.id_organizador = u.id_usuario
            WHERE v.id_organizador = %s
            ORDER BY v.fecha_inicio;
        """
        data = (id_organizador,)
        results = connectToPostgreSQL(DATABASE).query_db(query, data)
        partidos = []
        if results:
            for row in results:
                partidos.append(cls(row))
        return partidos

    # Método para validar los datos del partido
    @staticmethod
    def validar_partido(data):
        errores = []

        # Validar que los campos no estén vacíos
        if not data['lugar']:
            errores.append("El lugar es obligatorio")

        if not data['fecha_inicio']:
            errores.append("La fecha de inicio es obligatoria")

        if not data['descripcion']:
            errores.append("La descripcion es obligatorio")

        return errores

    @classmethod
    def last_insert_id(cls):
        return connectToPostgreSQL(DATABASE).query_db("SELECT LASTVAL() as id;")[0]['id']

    @classmethod
    def get_participantes_partidos(cls, datos):
        query = "SELECT * FROM partidos LEFT JOIN participantes ON participantes.partido_id = partidos.id_partido WHERE partidos.id_partido = %s;"
        data = (datos['id_partido'],)
        resultados = connectToPostgreSQL(DATABASE).query_db(
            query, data)  # Consulta a la base de datos
        partido = cls(resultados[0])  # Creamos una instancia de Partido
        for fila_en_db in resultados:
            if fila_en_db['participantes.id_participante'] is not None:
                datos_participante = {
                    "id": fila_en_db['participantes.id_participante'],
                    "nombre": fila_en_db['participantes.nombre'],
                    "apellido": fila_en_db['apellido'],
                    "created_at": fila_en_db['created_at'],
                    "updated_at": fila_en_db['updated_at'],
                    "partido_id": fila_en_db['id_partido']
                }
                # Agregando un nuevo participante a la lista de participantes del partido
                partido.participantes.append(
                    participante.Participante(datos_participante))
        return partido

    @classmethod
    def obtener_participantes(cls, id_partido):
        query = """
            SELECT p.*, u.nombre 
            FROM participantes_partido p
            JOIN usuarios u ON p.id_usuario = u.id_usuario
            WHERE p.id_partido = %s;
        """
        data = (id_partido,)
        results = connectToPostgreSQL(DATABASE).query_db(query, data)
        participantes = []
        if results:
            for row in results:
                participantes.append(row)

        for participante in participantes:
            # Acceder a los atributos de cada participante
            print("Datos del participante:", participante)

        return participantes
