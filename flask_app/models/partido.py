# modelos/viaje.py
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import participante
DATABASE = 'nosfalta1'
class Partido:
    def __init__(self, data):
        self.id_partido = data['id_partido']
        self.lugar = data['lugar']
        self.fecha_inicio = data['fecha_inicio']
        self.descripcion = data['descripcion']
        self.id_organizador = data['id_organizador']
        self.id_localidad = data.get('id_localidad', None)  # Usar .get para evitar KeyError
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
        resultado = connectToMySQL(DATABASE).query_db(query)
        partidos = []
        if resultado:
            for partido in resultado:
                #cls.get_participantes_partidos({'id_partido': partido['id_partido']})
                #print("Participantes:************ \n",type(participante.Participante.obtener_participantes_por_partido(partido['id_partido'])))
                cls(partido).participantes = participante.Participante.obtener_participantes_por_partido(partido['id_partido'])
                partidos.append(cls(partido))
        return partidos
    
    @classmethod
    def get_match_disponibles(cls, id_usuario):
        query = """
            SELECT p.*, u.nombre as organizador
            FROM partidos p
            JOIN usuarios u ON p.id_organizador = u.id_usuario
            WHERE p.id_organizador != %(id_usuario)s
            ORDER BY p.fecha_inicio;
        """
        data = {'id_usuario': id_usuario}
        results = connectToMySQL(DATABASE).query_db(query, data)
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
            WHERE p.id_partido = %(id_partido)s;
        """
        data = {'id_partido': id_partido}
        results = connectToMySQL(DATABASE).query_db(query, data)
        print("Obtener por id")
        print(results)
        return cls(results[0]) if results else None

    @classmethod
    def crear(cls, data):
        query = """
            INSERT INTO partidos (lugar, fecha_inicio, descripcion, id_organizador)
            VALUES (%(lugar)s, %(fecha_inicio)s, %(descripcion)s, %(id_organizador)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def actualizar(cls, data):
        query = """
            UPDATE partidos 
            SET lugar = %(lugar)s,
                fecha_inicio = %(fecha_inicio)s,
                descripcion = %(descripcion)s
            WHERE id = %(id)s;
        """
        query2 = """ UPDATE participantes SET id_participante = %(id_participante)s WHERE id_partido = %(id_partido)s;"""
        
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def eliminar(cls, id_partido):
        query1 = "DELETE FROM participantes_partido WHERE id_partido = %(id_partido)s;"
        query2 = "DELETE FROM partidos WHERE id_partido = %(id_partido)s;"
        data = {'id_partido': id_partido}
        connectToMySQL(DATABASE).query_db(query1, data)
        connectToMySQL(DATABASE).query_db(query2, data)
        return True

    @classmethod
    def obtener_por_organizador(cls, id_organizador):
        query = """
            SELECT v.*, u.nombre as organizador 
            FROM partidos v
            JOIN usuarios u ON v.id_organizador = u.id_usuario
            WHERE v.id_organizador = %(id_organizador)s
            ORDER BY v.fecha_inicio;
        """
        data = {'id_organizador': id_organizador}
        results = connectToMySQL(DATABASE).query_db(query, data)
        partidos = []
        if results:
            for row in results:
                partidos.append(cls(row))
        return partidos

    # Método para validar los datos del partido
    @staticmethod
    def validar_partido(data):
        errores = []
        
        if not data['fecha_inicio']:
            errores.append("La fecha de inicio es obligatoria")
            
        if not data['descripcion']:
            errores.append("La descripcion es obligatorio")

        return errores
    
    @classmethod
    def last_insert_id(cls):
        return connectToMySQL(DATABASE).query_db("SELECT LAST_INSERT_ID() as id;")[0]['id']
    

    @classmethod
    def get_participantes_partidos(cls, datos):
        query = "SELECT * FROM partidos LEFT JOIN participantes ON participantes.partido_id = partidos.id WHERE partidos.id = %(id_partido)s;"
        resultados = connectToMySQL(DATABASE).query_db(query, datos) #Consulta a la base de datos
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
                partido.participantes.append(participante.Participante(datos_participante)) 
        return partido
    
    @classmethod
    def obtener_participantes(cls, id_partido):
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