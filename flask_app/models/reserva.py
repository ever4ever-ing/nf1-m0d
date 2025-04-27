import logging
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, jsonify
from datetime import datetime, timedelta

from flask_app.models.cancha import Cancha
DATABASE = 'nosfalta1'

class Reserva:
    def __init__(self, data):
        self.id_reserva = data['id_reserva']
        self.id_cancha = data['id_cancha']
        self.id_usuario = data['id_usuario']
        self.fecha_reserva = data['fecha_reserva']
        self.hora_inicio = data['hora_inicio']
        self.hora_fin = data['hora_fin']
        self.fecha_creacion = data['fecha_creacion']
        self.fecha_actualizacion = data['fecha_actualizacion']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM reservas;"
        resultados = connectToMySQL(DATABASE).query_db(query)
        reservas = []
        for reserva in resultados:
            reservas.append(cls(reserva))
        return reservas

    @classmethod
    def save(cls, data):
        try:
            query = """
            INSERT INTO reservas (id_cancha, id_usuario, fecha_reserva, hora_inicio, hora_fin)
            VALUES (%(id_cancha)s, %(id_usuario)s, %(fecha_reserva)s, %(hora_inicio)s, %(hora_fin)s);
            """
            return connectToMySQL(DATABASE).query_db(query, data)
        except Exception as e:
            logging.error(f"Error al guardar reserva: {str(e)}")
            flash(f"Error al guardar la reserva. Por favor, contacte al administrador.", "danger")
            return False

    @staticmethod
    def validar_reserva(data):
        is_valid = True
        
        # Validar que los campos necesarios estén presentes
        if not data.get('fecha_reserva') or not data.get('hora_inicio') or not data.get('hora_fin'):
            flash('Fecha y horas son obligatorias', 'danger')
            return False
        
        # Validar que la fecha no sea en el pasado
        try:
            fecha_reserva = datetime.strptime(data['fecha_reserva'], '%Y-%m-%d').date()
            if fecha_reserva < datetime.now().date():
                flash('No se pueden realizar reservas en fechas pasadas', 'danger')
                return False
                
            # Validar que la hora de inicio sea válida (8:00 - 22:00)
            hora_inicio = data['hora_inicio']
            # Extraer solo el valor numérico de la hora independientemente del formato
            hora_valor = Reserva._extract_hour_value(hora_inicio)
                
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
        query = """
        SELECT * FROM reservas
        WHERE id_cancha = %(id_cancha)s 
        AND DATE(fecha_reserva) = %(fecha_reserva)s
        AND (
            (hora_inicio < %(hora_fin)s AND hora_fin > %(hora_inicio)s)
            OR (hora_inicio = %(hora_inicio)s)
            OR (hora_fin = %(hora_fin)s)
        );
        """
        resultado = connectToMySQL(DATABASE).query_db(query, data)
        if resultado:
            flash('La cancha ya está reservada en este horario', 'danger')
            return False
            
        return True

    @staticmethod
    def _extract_hour_value(hora):
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
                # Si todo lo demás falla, convertir a string y luego procesar
                hora_str = str(hora)
                if ':' in hora_str:
                    return int(hora_str.split(':')[0])
                else:
                    return int(hora_str)
        except Exception as e:
            logging.error(f"Error en extract_hour_value: {str(e)} - Tipo: {type(hora)}")
            # Devolver un valor predeterminado que pueda ser identificado claramente como error
            return -1

    @staticmethod
    def get_reservas_by_view(data, fechas):
        reservas = {}
        canchas = Cancha.get_all()
        
        for fecha in fechas:
            reservas[fecha.strftime('%Y-%m-%d')] = {}
            for cancha in canchas:
                reservas[fecha.strftime('%Y-%m-%d')][cancha.id_cancha] = Reserva.get_reservas_for_cancha_and_date(cancha.id_cancha, fecha)
        
        return reservas, canchas

    @staticmethod
    def get_reservas_for_cancha_and_date(cancha_id, fecha):
        query = """
        SELECT r.id_reserva, r.id_cancha, r.id_usuario, r.fecha_reserva, r.hora_inicio, r.hora_fin, u.nombre AS usuario_nombre
        FROM reservas r
        JOIN usuarios u ON r.id_usuario = u.id_usuario
        WHERE r.id_cancha = %(cancha_id)s AND DATE(r.fecha_reserva) = %(fecha)s;
        """
        data = {
            'cancha_id': cancha_id,
            'fecha': fecha.strftime('%Y-%m-%d')
        }
        resultados = connectToMySQL(DATABASE).query_db(query, data)
        reservas = {}
        for resultado in resultados:
            try:
                hora_inicio = Reserva._extract_hour_value(resultado['hora_inicio'])
                
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
    def get_by_id(cls, id_reserva):
        query = "SELECT * FROM reservas WHERE id_reserva = %(id_reserva)s;"
        result = connectToMySQL(DATABASE).query_db(query, {'id_reserva': id_reserva})
        if result:
            return cls(result[0])
        return None
    
    @classmethod
    def get_by_user_id(cls, id_usuario):
        query = """
        SELECT r.*, c.nombre as cancha_nombre
        FROM reservas r
        JOIN canchas c ON r.id_cancha = c.id_cancha
        WHERE r.id_usuario = %(id_usuario)s
        ORDER BY r.fecha_reserva DESC, r.hora_inicio;
        """
        results = connectToMySQL(DATABASE).query_db(query, {'id_usuario': id_usuario})
        reservas = []
        for row in results:
            reserva = cls(row)
            reserva.cancha_nombre = row['cancha_nombre']
            reservas.append(reserva)
        return reservas

    @classmethod
    def get_reservas_mensuales(cls, id_usuario, year, month):
        """Obtiene todas las reservas de un usuario en un mes específico simplificado"""
        query = """
        SELECT r.*, c.nombre as cancha_nombre, DAY(r.fecha_reserva) as dia
        FROM reservas r
        JOIN canchas c ON r.id_cancha = c.id_cancha
        WHERE r.id_usuario = %(id_usuario)s
        AND YEAR(r.fecha_reserva) = %(year)s
        AND MONTH(r.fecha_reserva) = %(month)s
        ORDER BY r.fecha_reserva, r.hora_inicio;
        """
        data = {
            'id_usuario': id_usuario,
            'year': year,
            'month': month
        }
        
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        # Simplificar: solo contar reservas por día
        reservas_por_dia = {}
        for row in results:
            dia = row['dia']
            if dia not in reservas_por_dia:
                reservas_por_dia[dia] = []
                
            # Convertir a clase reserva para mantener consistencia
            reserva = cls(row)
            reserva.cancha_nombre = row['cancha_nombre']
            reservas_por_dia[dia].append(reserva)
            
        return reservas_por_dia

    @classmethod
    def delete(cls, id_reserva):
        query = "DELETE FROM reservas WHERE id_reserva = %(id_reserva)s;"
        return connectToMySQL(DATABASE).query_db(query, {'id_reserva': id_reserva})
