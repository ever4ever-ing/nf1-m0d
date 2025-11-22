# modelos/viaje.py
import logging
from flask_app.models import participante
from flask_app.models.localidad import Localidad
from flask_app.models.reserva import Reserva
from flask_app.config.mysqlconnection import connectToMySQL, DB_HOST, DB_USER, DB_PASSWORD, DATABASE

import os
from dotenv import load_dotenv
load_dotenv()
DATABASE = os.getenv('MYSQL_DATABASE')
class Partido:
    def __init__(self, data):
        self.id_partido = data['id_partido']
        self.lugar = data.get('lugar', None)  # Usar .get para evitar KeyError
        self.fecha_inicio = data.get('fecha_inicio', None)  # Usar .get para permitir NULL
        self.descripcion = data['descripcion']
        self.max_jugadores = data.get('max_jugadores', 10)  # Valor por defecto 10
        self.id_organizador = data['id_organizador']
        # Usar .get para evitar KeyError
        self.id_localidad = data.get('id_localidad', None)
        # Usar .get para evitar KeyError
        self.id_reserva = data.get('id_reserva', None)
        self.fecha_creacion = data['fecha_creacion']
        self.fecha_actualizacion = data['fecha_actualizacion']
        self.organizador = data.get('organizador', None)
        self.participantes = []

    @classmethod
    def get_all(cls):
        query = """
            SELECT v.*, u.nombre as organizador,
                   r.fecha_reserva, r.hora_inicio as reserva_hora_inicio, r.hora_fin as reserva_hora_fin,
                   c.nombre as cancha_nombre, rec.nombre as recinto_nombre
            FROM partidos v
            JOIN usuarios u ON v.id_organizador = u.id_usuario
            LEFT JOIN reservas r ON v.id_reserva = r.id_reserva
            LEFT JOIN canchas c ON r.id_cancha = c.id_cancha
            LEFT JOIN recintos rec ON r.id_recinto = rec.id_recinto
            ORDER BY v.fecha_inicio;
        """
        resultado = connectToMySQL(DATABASE).query_db(query)
        partidos = []
        if resultado:
            for partido_data in resultado:
                partido_obj = cls(partido_data)
                partido_obj.participantes = participante.Participante.obtener_participantes_por_partido(
                    partido_data['id_partido'])
                # Agregar información de la reserva si existe
                if partido_data.get('fecha_reserva'):
                    partido_obj.reserva_info = {
                        'fecha_reserva': partido_data['fecha_reserva'],
                        'hora_inicio': partido_data['reserva_hora_inicio'],
                        'hora_fin': partido_data['reserva_hora_fin'],
                        'cancha_nombre': partido_data['cancha_nombre'],
                        'recinto_nombre': partido_data['recinto_nombre']
                    }
                partidos.append(partido_obj)
        return partidos
        
    @classmethod
    def get_match_disponibles(cls, id_usuario):
        query = """
            SELECT p.*, u.nombre as organizador, l.nombre as localidad_nombre
            FROM partidos p
            JOIN usuarios u ON p.id_organizador = u.id_usuario
            LEFT JOIN localidades l ON p.id_localidad = l.id_localidad
            WHERE p.id_organizador != %(id_usuario)s
            ORDER BY p.fecha_inicio;
        """
        data = {'id_usuario': id_usuario}
        results = connectToMySQL(DATABASE).query_db(query, data)
        partidos = []
        if results:
            for row in results:
                partido = cls(row)
                # Añadimos los participantes a cada partido
                partido.participantes = cls.obtener_participantes(partido.id_partido)
                partidos.append(partido)
        return partidos

    @classmethod
    def obtener_por_id(cls, id_partido):
        query = """
            SELECT p.*, u.nombre as organizador,
                   r.fecha_reserva, r.hora_inicio as reserva_hora_inicio, r.hora_fin as reserva_hora_fin,
                   c.nombre as cancha_nombre, rec.nombre as recinto_nombre
            FROM partidos p
            JOIN usuarios u ON p.id_organizador = u.id_usuario
            LEFT JOIN reservas r ON p.id_reserva = r.id_reserva
            LEFT JOIN canchas c ON r.id_cancha = c.id_cancha
            LEFT JOIN recintos rec ON r.id_recinto = rec.id_recinto
            WHERE p.id_partido = %(id_partido)s;
        """
        data = {'id_partido': id_partido}
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            partido = cls(results[0])
            # Agregar información de la reserva si existe
            if results[0].get('fecha_reserva'):
                partido.reserva_info = {
                    'fecha_reserva': results[0]['fecha_reserva'],
                    'hora_inicio': results[0]['reserva_hora_inicio'],
                    'hora_fin': results[0]['reserva_hora_fin'],
                    'cancha_nombre': results[0]['cancha_nombre'],
                    'recinto_nombre': results[0]['recinto_nombre']
                }
            return partido
        return None

    @classmethod
    def crear(cls, data):
        # Obtener el nombre de la localidad
        lugar = Localidad.obtener_por_id(data['id_localidad'])
        if lugar:
            logging.debug(f"Localidad encontrada: {lugar.nombre}")
            data['lugar'] = lugar.nombre
        else:
            logging.error(
                f"partido.py En crear: No se encontró localidad con id {data['id_localidad']}")
            data['lugar'] = None
        
        # Asegurar que fecha_inicio esté en data, aunque sea None
        if 'fecha_inicio' not in data or not data['fecha_inicio']:
            data['fecha_inicio'] = None
            logging.debug("fecha_inicio no proporcionada, se establecerá como NULL")
        
        # Asegurar que descripcion esté en data, aunque sea vacía
        if 'descripcion' not in data or not data['descripcion']:
            data['descripcion'] = ''
            logging.debug("descripcion no proporcionada, se establecerá como cadena vacía")
        
        # Asegurar que max_jugadores esté en data
        if 'max_jugadores' not in data or not data['max_jugadores']:
            data['max_jugadores'] = 10
            logging.debug("max_jugadores no proporcionado, se establecerá como 10")
        
        query = """
            INSERT INTO partidos (lugar, fecha_inicio, descripcion, max_jugadores, id_organizador, id_localidad)
            VALUES (%(lugar)s, %(fecha_inicio)s, %(descripcion)s, %(max_jugadores)s, %(id_organizador)s, %(id_localidad)s);
        """
        # Ejecutar la consulta y obtener el resultado
        resultado = connectToMySQL(DATABASE).query_db(query, data)
        logging.debug(f"Resultado de la consulta al crear: {resultado}")
        #print("Resultado:", resultado)
        # Verificar si se obtuvo un resultado y devolver el id_partido
        return resultado  # Devuelve el id_partido generado o None si no hay resultado


    @classmethod
    def actualizar(cls, data):
        # Construir query dinámicamente basado en campos presentes
        campos_actualizar = []
        
        if 'fecha_inicio' in data:
            campos_actualizar.append("fecha_inicio = %(fecha_inicio)s")
        if 'descripcion' in data:
            campos_actualizar.append("descripcion = %(descripcion)s")
        if 'max_jugadores' in data:
            campos_actualizar.append("max_jugadores = %(max_jugadores)s")
        if 'id_reserva' in data:
            campos_actualizar.append("id_reserva = %(id_reserva)s")
        
        if not campos_actualizar:
            logging.warning("No hay campos para actualizar")
            return False
        
        query = f"""
            UPDATE partidos 
            SET {', '.join(campos_actualizar)}
            WHERE id_partido = %(id_partido)s;
        """

        try:
            resultado = connectToMySQL(DATABASE).query_db(query, data)
            logging.info(f"Partido {data['id_partido']} actualizado exitosamente")
            return True
        except Exception as e:
            logging.error(f"Error al actualizar partido: {e}")
            return False

    @classmethod
    def eliminar(cls, id_partido):
        """
        Elimina un partido y todos sus datos relacionados (reserva y participantes)
        
        Parameters:
            id_partido (int): ID del partido a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            data = {'id_partido': id_partido}
            
            # Primero, obtener el id_reserva del partido (si existe)
            query_get_reserva = "SELECT id_reserva FROM partidos WHERE id_partido = %(id_partido)s;"
            resultado = connectToMySQL(DATABASE).query_db(query_get_reserva, data)
            
            # Si existe una reserva asociada, eliminarla ANTES de eliminar el partido
            if resultado and resultado[0]['id_reserva']:
                id_reserva = resultado[0]['id_reserva']
                logging.info(f"Partido {id_partido} tiene reserva asociada: {id_reserva}")
                
                # Usar el método eliminar de la clase Reserva
                if Reserva.eliminar(id_reserva):
                    logging.info(f"✓ Reserva {id_reserva} eliminada exitosamente")
                else:
                    logging.error(f"✗ Error al eliminar reserva {id_reserva}")
                    # Continuar con la eliminación del partido aunque falle la reserva
            else:
                logging.info(f"Partido {id_partido} no tiene reserva asociada")
            
            # Eliminar participantes del partido
            query1 = "DELETE FROM participantes_partido WHERE id_partido = %(id_partido)s;"
            connectToMySQL(DATABASE).query_db(query1, data)
            logging.info(f"✓ Participantes del partido {id_partido} eliminados")
            
            # Finalmente, eliminar el partido
            query2 = "DELETE FROM partidos WHERE id_partido = %(id_partido)s;"
            connectToMySQL(DATABASE).query_db(query2, data)
            
            logging.info(f"✓ Partido {id_partido} eliminado exitosamente")
            return True
            
        except Exception as e:
            logging.error(f"✗ Error al eliminar partido {id_partido}: {str(e)}")
            return False

    @classmethod
    def obtener_por_organizador(cls, id_organizador):
        query = """
            SELECT v.*, u.nombre as organizador,
                   r.fecha_reserva, r.hora_inicio as reserva_hora_inicio, r.hora_fin as reserva_hora_fin,
                   c.nombre as cancha_nombre, rec.nombre as recinto_nombre
            FROM partidos v
            JOIN usuarios u ON v.id_organizador = u.id_usuario
            LEFT JOIN reservas r ON v.id_reserva = r.id_reserva
            LEFT JOIN canchas c ON r.id_cancha = c.id_cancha
            LEFT JOIN recintos rec ON r.id_recinto = rec.id_recinto
            WHERE v.id_organizador = %(id_organizador)s
            ORDER BY v.fecha_inicio;
        """
        data = {'id_organizador': id_organizador}
        results = connectToMySQL(DATABASE).query_db(query, data)
        partidos = []
        if results:
            for row in results:
                partido_obj = cls(row)
                # Agregar información de la reserva si existe
                if row.get('fecha_reserva'):
                    partido_obj.reserva_info = {
                        'fecha_reserva': row['fecha_reserva'],
                        'hora_inicio': row['reserva_hora_inicio'],
                        'hora_fin': row['reserva_hora_fin'],
                        'cancha_nombre': row['cancha_nombre'],
                        'recinto_nombre': row['recinto_nombre']
                    }
                partidos.append(partido_obj)
        return partidos

    # Método para validar los datos del partido
    @staticmethod
    def validar_partido(data):
        errores = []

        # fecha_inicio ya no es obligatoria
        # if not data['fecha_inicio']:
        #     errores.append("La fecha de inicio es obligatoria")

        # descripcion ya no es obligatoria
        # if not data['descripcion']:
        #     errores.append("La descripcion es obligatorio")
        
        # Validar que id_localidad esté presente y sea válido
        if not data.get('id_localidad'):
            errores.append("La localidad es obligatoria")

        return errores

    @classmethod
    def last_insert_id(cls):
        return connectToMySQL(DATABASE).query_db("SELECT LAST_INSERT_ID() as id;")[0]['id']

    @classmethod
    def get_participantes_partidos(cls, datos):
        query = "SELECT * FROM partidos LEFT JOIN participantes ON participantes.partido_id = partidos.id WHERE partidos.id = %(id_partido)s;"
        resultados = connectToMySQL(DATABASE).query_db(
            query, datos)  # Consulta a la base de datos
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
                WHERE p.id_partido = %(id_partido)s;
            """
            data = {'id_partido': id_partido}
            results = connectToMySQL(DATABASE).query_db(query, data)
            #print(type(results))
            participantes = []
            if results:
                for row in results:
                    #print(row)
                    participantes.append(row)

            #for participante in participantes:
                # Acceder a los atributos de cada participante
                #print("Datos del participante:", participante)
            return participantes    
    @classmethod
    def get_partidos_by_localidad(cls, id_localidad):
        # Si id_localidad es 0 o None, mostrar todos los partidos de todas las localidades
        if id_localidad == 0 or id_localidad is None:
            query = """
                SELECT p.*, u.nombre as organizador, l.nombre as localidad_nombre,
                       r.fecha_reserva, r.hora_inicio as reserva_hora_inicio, r.hora_fin as reserva_hora_fin,
                       c.nombre as cancha_nombre, rec.nombre as recinto_nombre
                FROM partidos p
                JOIN usuarios u ON p.id_organizador = u.id_usuario
                LEFT JOIN localidades l ON p.id_localidad = l.id_localidad
                LEFT JOIN reservas r ON p.id_reserva = r.id_reserva
                LEFT JOIN canchas c ON r.id_cancha = c.id_cancha
                LEFT JOIN recintos rec ON r.id_recinto = rec.id_recinto
                ORDER BY p.fecha_inicio;
            """
            data = {}
            logging.debug("Mostrando TODOS los partidos de TODAS las localidades")
        else:
            query = """
                SELECT p.*, u.nombre as organizador, l.nombre as localidad_nombre,
                       r.fecha_reserva, r.hora_inicio as reserva_hora_inicio, r.hora_fin as reserva_hora_fin,
                       c.nombre as cancha_nombre, rec.nombre as recinto_nombre
                FROM partidos p
                JOIN usuarios u ON p.id_organizador = u.id_usuario
                LEFT JOIN localidades l ON p.id_localidad = l.id_localidad
                LEFT JOIN reservas r ON p.id_reserva = r.id_reserva
                LEFT JOIN canchas c ON r.id_cancha = c.id_cancha
                LEFT JOIN recintos rec ON r.id_recinto = rec.id_recinto
                WHERE p.id_localidad = %(id_localidad)s
                ORDER BY p.fecha_inicio;
            """
            data = {'id_localidad': id_localidad}
            logging.debug(f"Filtrando partidos por localidad ID: {id_localidad}")
        
        logging.debug(f"Consulta: {query}")
        logging.debug(f"Datos: {data}")
        
        results = connectToMySQL(DATABASE).query_db(query, data)
        partidos = []
        if results:
            logging.debug(f"Se encontraron {len(results)} partidos")
            for row in results:
                partido = cls(row)
                # Añadimos los participantes a cada partido
                partido.participantes = cls.obtener_participantes(partido.id_partido)
                # Agregar información de la reserva si existe
                if row.get('fecha_reserva'):
                    partido.reserva_info = {
                        'fecha_reserva': row['fecha_reserva'],
                        'hora_inicio': row['reserva_hora_inicio'],
                        'hora_fin': row['reserva_hora_fin'],
                        'cancha_nombre': row['cancha_nombre'],
                        'recinto_nombre': row['recinto_nombre']
                    }
                partidos.append(partido)
        else:
            logging.debug("No se encontraron partidos con los criterios de búsqueda")
            
        return partidos
