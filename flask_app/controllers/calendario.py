from flask import render_template, redirect, url_for, request, session, flash, jsonify
from flask_app import app
from flask_app.models.reserva import Reserva
from flask_calendar import Calendar, EventList
from datetime import datetime, date

calendar = Calendar()

@app.route('/fullcalendar')
def fullcalendar():
    if 'usuario_id' not in session:
        flash('Debe iniciar sesión para ver el calendario', 'warning')
        return redirect('/login')
    
    return render_template('fullcalendar.html')

@app.route('/api/events')
def get_events():
    """API endpoint para obtener eventos de reserva en formato FullCalendar"""
    if 'usuario_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    # Obtener todas las reservas del usuario
    user_reservas = Reserva.get_by_user_id(session['usuario_id'])
    
    # Formatear para FullCalendar
    events = []
    for reserva in user_reservas:
        fecha = reserva.fecha_reserva
        if isinstance(fecha, str):
            fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
            
        # Extraer hora de inicio y fin
        hora_inicio = str(reserva.hora_inicio)
        hora_fin = str(reserva.hora_fin)
        
        # Crear evento en formato FullCalendar
        event = {
            'id': reserva.id_reserva,
            'title': f'Cancha: {reserva.cancha_nombre}',
            'start': f"{fecha.strftime('%Y-%m-%d')}T{hora_inicio}",
            'end': f"{fecha.strftime('%Y-%m-%d')}T{hora_fin}",
            'backgroundColor': '#0d6efd',  # Color para las reservas
            'borderColor': '#0a58ca'
        }
        events.append(event)
    
    return jsonify(events)
