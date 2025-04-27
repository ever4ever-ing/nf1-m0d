import logging
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime, timedelta

from flask_app.models.cancha import Cancha
DATABASE = 'nosfalta1'

class Reserva:
    def __init__(self, data):
        self.id_reserva = data['id_reserva']
        self.id_cancha = data['id_cancha']
        self.id_usuario = data['id_usuario']
        self.fecha_reserva = data['fecha_reserva']
        self.fecha_creacion = data['fecha_creacion']
        self.fecha_actualizacion = data['fecha_actualizacion']  # Cambiado para reflejar la columna correcta

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
        query = """
        INSERT INTO reservas (id_cancha, id_usuario, fecha_reserva)
        VALUES (%(id_cancha)s, %(id_usuario)s, %(fecha_reserva)s);
        """
        # No se incluye fecha_creacion ni fecha_actualizacion porque tienen valores predeterminados
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, id_reserva):
        query = "DELETE FROM reservas WHERE id_reserva = %(id_reserva)s;"
        return connectToMySQL(DATABASE).query_db(query, {'id_reserva': id_reserva})

    @staticmethod
    def validar_reserva(data):
        if not data['fecha_reserva']:
            flash('Fecha es obligatoria', 'error')
            return False
        # Validar si ya existe una reserva en el mismo horario
        query = """
        SELECT * FROM reservas
        WHERE id_cancha = %(id_cancha)s AND fecha_reserva = %(fecha_reserva)s;
        """
        # Eliminado hora_reserva porque no está en la estructura de la base de datos
        resultado = connectToMySQL(DATABASE).query_db(query, data)
        if resultado:
            flash('La cancha ya está reservada en este horario', 'error')
            return False
        return True

    @classmethod
    def check_availability(cls, cancha_id, start_date, end_date):
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido"}), 400

        query = """
        SELECT * FROM reservas
        WHERE id_cancha = %(cancha_id)s AND fecha_reserva BETWEEN %(start_date)s AND %(end_date)s;
        """
        # Eliminado hora_reserva porque no está en la estructura de la base de datos
        data = {'cancha_id': cancha_id, 'start_date': start_date, 'end_date': end_date}
        reservas = connectToMySQL(DATABASE).query_db(query, data)
        disponibilidad = []
        for reserva in reservas:
            disponibilidad.append({
                "fecha_reserva": reserva['fecha_reserva'],
                "usuario_nombre": reserva['usuario_nombre']  # Asegurarse de que este campo esté en la consulta
            })
        return jsonify(disponibilidad)

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
        SELECT r.id_reserva, r.id_cancha, r.id_usuario, r.fecha_reserva, u.nombre AS usuario_nombre
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
            hora = resultado['fecha_reserva'].hour
            reservas[hora] = {
                'id_reserva': resultado['id_reserva'],
                'usuario_nombre': resultado['usuario_nombre']
            }
        return reservas
