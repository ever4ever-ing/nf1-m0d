import logging
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, jsonify
from datetime import datetime, timedelta

from flask_app.models.cancha import Cancha
BASE_DATOS = 'nosfalta1'

class Reserva:
    def __init__(self, datos):
        self.id_reserva = datos['id_reserva']
        self.id_cancha = datos['id_cancha']
        self.id_usuario = datos['id_usuario']
        self.fecha_reserva = datos['fecha_reserva']
        self.hora_inicio = datos['hora_inicio']
        self.hora_fin = datos['hora_fin']
        self.fecha_creacion = datos['fecha_creacion']
        self.fecha_actualizacion = datos['fecha_actualizacion']

    @classmethod
    def obtener_todas(cls):
        consulta = "SELECT * FROM reservas;"
        resultados = connectToMySQL(BASE_DATOS).query_db(consulta)
        reservas = []
        for reserva in resultados:
            reservas.append(cls(reserva))
        return reservas

    @classmethod
    def guardar(cls, datos):
        try:
            consulta = """
            INSERT INTO reservas (id_cancha, id_usuario, fecha_reserva, hora_inicio, hora_fin)
            VALUES (%(id_cancha)s, %(id_usuario)s, %(fecha_reserva)s, %(hora_inicio)s, %(hora_fin)s);
            """
            return connectToMySQL(BASE_DATOS).query_db(consulta, datos)
        except Exception as e:
            logging.error(f"Error al guardar reserva: {str(e)}")
            flash(f"Error al guardar la reserva. Por favor, contacte al administrador.", "danger")
            return False

    @staticmethod
    def validar_reserva(datos):
        es_valido = True
        
        # Validar que los campos necesarios estén presentes
        if not datos.get('fecha_reserva') or not datos.get('hora_inicio') or not datos.get('hora_fin'):
            flash('Fecha y horas son obligatorias', 'danger')
            return False
        
        # Validar que la fecha no sea en el pasado
        try:
            fecha_reserva = datetime.strptime(datos['fecha_reserva'], '%Y-%m-%d').date()
            if fecha_reserva < datetime.now().date():
                flash('No se pueden realizar reservas en fechas pasadas', 'danger')
                return False
                
            # Validar que la hora de inicio sea válida (8:00 - 22:00)
            hora_inicio = datos['hora_inicio']
            hora_valor = Reserva._extraer_valor_hora(hora_inicio)
                
            if hora_valor < 8 or hora_valor > 22:
                flash('El horario de reservas es de 8:00 a 22:00', 'danger')
                return False
                
        except ValueError as e:
            flash(f'Formato de fecha u hora inválido: {str(e)}', 'danger')
            return False
        except Exception as e:
            flash(f'Error al validar reserva: {str(e)}', 'danger')
            return False
        
        # Verificar si la cancha ya está reservada en ese horario
        consulta = """
        SELECT * FROM reservas
        WHERE id_cancha = %(id_cancha)s 
        AND DATE(fecha_reserva) = %(fecha_reserva)s
        AND (
            (hora_inicio < %(hora_fin)s AND hora_fin > %(hora_inicio)s)
            OR (hora_inicio = %(hora_inicio)s)
            OR (hora_fin = %(hora_fin)s)
        );
        """
        resultado = connectToMySQL(BASE_DATOS).query_db(consulta, datos)
        if resultado:
            flash('La cancha ya está reservada en este horario', 'danger')
            return False
            
        return True
    @classmethod
    def obtener_por_canchas(cls, ids_canchas, fecha=None):
        """
        Obtiene las reservas para un conjunto de canchas con una sola consulta
        
        Parameters:
            ids_canchas (list): Lista de IDs de canchas
            fecha (datetime.date, optional): Fecha para filtrar las reservas
            
        Returns:
            dict: Diccionario donde las claves son los IDs de cancha y los valores son listas de reservas
        """
        if not ids_canchas:
            return {}
        
        # Crear la lista de IDs para la consulta
        ids_str = ','.join(str(id_cancha) for id_cancha in ids_canchas)
        
        # Base de la consulta
        consulta = f"""
        SELECT r.*, c.nombre as cancha_nombre
        FROM reservas r
        JOIN canchas c ON r.id_cancha = c.id_cancha
        WHERE r.id_cancha IN ({ids_str})
        """
        
        # Parámetros para la consulta
        params = {}
        
        # Agregar filtro por fecha si se proporciona
        if fecha:
            consulta += " AND DATE(r.fecha_reserva) = %(fecha)s"
            params['fecha'] = fecha.strftime('%Y-%m-%d') if not isinstance(fecha, str) else fecha
        
        # Ordenar resultados
        consulta += " ORDER BY r.id_cancha, r.hora_inicio;"
        
        # Ejecutar consulta
        resultados = connectToMySQL(BASE_DATOS).query_db(consulta, params)
        
        # Organizar resultados por cancha
        reservas_por_cancha = {id_cancha: [] for id_cancha in ids_canchas}
        
        if resultados and isinstance(resultados, list):
            for fila in resultados:
                reserva = cls(fila)
                reserva.cancha_nombre = fila['cancha_nombre']
                reservas_por_cancha[fila['id_cancha']].append(reserva)
        
        # Añadir esta línea para devolver el resultado
        return reservas_por_cancha

    @staticmethod
    def _extraer_valor_hora(hora):
        """Método auxiliar para extraer el valor numérico de hora de diferentes formatos"""
        try:
            if isinstance(hora, int):
                return hora
            elif isinstance(hora, str):
                if ':' in hora:
                    return int(hora.split(':')[0])
                else:
                    return int(hora)
            elif hasattr(hora, 'hour'):  # Para objetos datetime.time y datetime.datetime
                return hora.hour
            elif hasattr(hora, 'total_seconds'):  # Para objetos datetime.timedelta
                return int(hora.total_seconds() // 3600)
            else:
                hora_str = str(hora)
                if ':' in hora_str:
                    return int(hora_str.split(':')[0])
                else:
                    return int(hora_str)
        except Exception as e:
            logging.error(f"Error en extraer_valor_hora: {str(e)} - Tipo: {type(hora)}")
            return -1


    @staticmethod
    def obtener_reservas_por_fecha(id_cancha, fecha):
        consulta = """
        SELECT r.id_reserva, r.id_cancha, r.id_usuario, r.fecha_reserva, r.hora_inicio, r.hora_fin, u.nombre AS usuario_nombre
        FROM reservas r
        JOIN usuarios u ON r.id_usuario = u.id_usuario
        WHERE r.id_cancha = %(id_cancha)s AND DATE(r.fecha_reserva) = %(fecha)s;
        """
        datos = {
            'fecha': fecha.strftime('%Y-%m-%d')
        }
        resultados = connectToMySQL(BASE_DATOS).query_db(consulta, datos)
        reservas = {}
        for resultado in resultados:
            try:
                hora_inicio = Reserva._extraer_valor_hora(resultado['hora_inicio'])
                
                reservas[hora_inicio] = {
                    'id_reserva': resultado['id_reserva'],
                    'id_usuario': resultado['id_usuario'],
                    'usuario_nombre': resultado['usuario_nombre'],
                    'hora_inicio': resultado['hora_inicio'],
                    'hora_fin': resultado['hora_fin']
                }
            except Exception as e:
                logging.error(f"Error al procesar hora: {str(e)} - Tipo: {type(resultado['hora_inicio'])}")
                continue
                
        return reservas

    @classmethod
    def obtener_por_id(cls, id_reserva):
        consulta = "SELECT * FROM reservas WHERE id_reserva = %(id_reserva)s;"
        resultado = connectToMySQL(BASE_DATOS).query_db(consulta, {'id_reserva': id_reserva})
        if resultado:
            return cls(resultado[0])
        return None
    
    @classmethod
    def obtener_por_usuario(cls, id_usuario):
        consulta = """
        SELECT r.*, c.nombre as cancha_nombre
        FROM reservas r
        JOIN canchas c ON r.id_cancha = c.id_cancha
        WHERE r.id_usuario = %(id_usuario)s
        ORDER BY r.fecha_reserva DESC, r.hora_inicio;
        """
        resultados = connectToMySQL(BASE_DATOS).query_db(consulta, {'id_usuario': id_usuario})
        reservas = []
        for fila in resultados:
            reserva = cls(fila)
            reserva.cancha_nombre = fila['cancha_nombre']
            reservas.append(reserva)
        return reservas


    @classmethod
    def eliminar(cls, id_reserva):
        consulta = "DELETE FROM reservas WHERE id_reserva = %(id_reserva)s;"
        return connectToMySQL(BASE_DATOS).query_db(consulta, {'id_reserva': id_reserva})
