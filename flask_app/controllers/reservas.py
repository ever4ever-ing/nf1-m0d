from flask import render_template, redirect, url_for, flash, jsonify, request, session
from flask_app.models.cancha import Cancha  # Asegúrate de que esta línea esté presente
from flask_app.models.reserva import Reserva
from flask_app import app
from datetime import datetime, timedelta

@app.route('/reservas')
def reserva():
    if 'usuario_id' not in session:
        return redirect('/login')
    
    view_type = request.args.get('view_type', 'day')  # Vista predeterminada: "diaria"
    selected_date = request.args.get('selected_date', datetime.now().date().strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    
    # Generar fechas para la vista diaria
    if view_type == 'day':
        fechas = [selected_date]  # Mostrar solo la fecha seleccionada
    else:
        fechas = []  # Otras vistas no se manejan en este caso

    # Validar que fechas no esté vacío
    if not fechas:
        flash('No se encontraron fechas disponibles.', 'warning')
        return redirect(url_for('index'))

    data = {
        'view_type': view_type,
        'selected_date': selected_date
    }
    reservas, canchas = Reserva.get_reservas_by_view(data, fechas)
    
    return render_template('agenda.html', canchas=canchas, fechas=fechas, reservas=reservas, view_type=view_type, selected_date=selected_date)

@app.route('/reserve/<int:cancha_id>/<date>/<time>', methods=['GET', 'POST'])
def reserve(cancha_id, date, time):
    if 'usuario_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        data = {
            'id_cancha': cancha_id,
            'id_usuario': session['usuario_id'],
            'fecha_reserva': date,
            'hora_reserva': time
        }
        if not Reserva.validar_reserva(data):
            return redirect(url_for('index'))
        Reserva.save(data)
        flash('Reserva realizada con éxito', 'success')
        return redirect(url_for('index'))
    return render_template('agenda.html', cancha_id=cancha_id, date=date, time=time)

@app.route('/delete_reservation/<int:reservation_id>', methods=['POST'])
def delete_reservation(reservation_id):
    if 'usuario_id' not in session:
        return redirect('/login')
    Reserva.delete(reservation_id)
    flash('Reserva eliminada con éxito', 'success')
    return redirect(url_for('index'))

@app.route('/api/availability', methods=['GET'])
def api_availability():
    selected_date = request.args.get('selected_date')
    if not selected_date:
        return jsonify({'error': 'Fecha no proporcionada'}), 400

    selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    fechas = [selected_date]
    data = {
        'view_type': 'day',
        'selected_date': selected_date
    }
    reservas, canchas = Reserva.get_reservas_by_view(data, fechas)

    # Renderizar solo la tabla de disponibilidad
    html = render_template('partials/availability_table.html', canchas=canchas, reservas=reservas, selected_date=selected_date)
    return jsonify({'html': html})

@app.route('/mostrar_reservas')
def mostrar_reservas():
    return redirect(url_for('reserva'))

@app.route('/crear_reserva/<int:cancha_id>/<date>/<int:hour>', methods=['POST'])
def crear_reserva(cancha_id, date, hour):
    if 'usuario_id' not in session:
        return redirect('/login')
    data = {
        'id_cancha': cancha_id,
        'id_usuario': session['usuario_id'],
        'fecha_reserva': date,
        'hora_reserva': hour
    }
    if not Reserva.validar_reserva(data):
        flash('No se pudo realizar la reserva. Verifique la disponibilidad.', 'danger')
        return redirect(url_for('reserva'))
    Reserva.save(data)
    flash('Reserva creada con éxito', 'success')
    return redirect(url_for('reserva'))