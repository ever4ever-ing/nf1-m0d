from flask import render_template, redirect, url_for, flash, jsonify, request, session
from flask_app.models.cancha import Cancha
from flask_app.models.reserva import Reserva
from flask_app import app
from datetime import datetime, timedelta
import logging

@app.route('/reservas')
def reserva():
    if 'usuario_id' not in session:
        flash('Debe iniciar sesión para ver las reservas', 'warning')
        return redirect('/login')

    selected_date = request.args.get(
        'selected_date', datetime.now().date().strftime('%Y-%m-%d'))
    try:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        selected_date = datetime.now().date()

    # Solo vista por día
    fechas = [selected_date]

    data = {
        'view_type': 'day',
        'selected_date': selected_date
    }

    reservas, canchas = Reserva.get_reservas_by_view(data, fechas)

    return render_template('agenda.html',
                           canchas=canchas,
                           fechas=fechas,
                           reservas=reservas,
                           selected_date=selected_date)


@app.route('/crear_reserva_simple', methods=['POST'])
def crear_reserva_simple():
    if 'usuario_id' not in session:
        flash('Debe iniciar sesión para realizar una reserva', 'warning')
        return redirect('/login')

    try:
        # Obtener datos del formulario
        cancha_id = request.form.get('cancha_id')
        fecha_reserva = request.form.get('fecha_reserva')
        
        # Asegurarse de que hora_inicio sea un entero
        try:
            hora_inicio = int(request.form.get('hora_inicio'))
            hora_fin = hora_inicio + 1
        except (TypeError, ValueError):
            flash('Formato de hora inválido', 'danger')
            return redirect(url_for('reserva'))

        # Validaciones básicas
        if not cancha_id or not fecha_reserva or hora_inicio is None:
            flash('Todos los campos son requeridos', 'danger')
            return redirect(url_for('reserva', selected_date=fecha_reserva))

        # Preparar datos para la reserva - asegurarse de que sean strings para SQL
        data = {
            'id_cancha': cancha_id,
            'id_usuario': session['usuario_id'],
            'fecha_reserva': fecha_reserva,
            'hora_inicio': f'{hora_inicio:02d}:00:00',
            'hora_fin': f'{hora_fin:02d}:00:00'
        }
        
        # Validar y guardar en la base de datos
        if Reserva.validar_reserva(data):
            reserva_id = Reserva.save(data)
            if reserva_id:
                flash(f'Reserva creada exitosamente para el {fecha_reserva} a las {hora_inicio}:00', 'success')
            else:
                flash('Error al guardar la reserva en la base de datos', 'danger')
        
    except Exception as e:
        flash(f'Error inesperado: {str(e)}', 'danger')
        logging.error(f"Error en crear_reserva_simple: {str(e)}")
    
    return redirect(url_for('reserva', selected_date=fecha_reserva if 'fecha_reserva' in locals() else None))


@app.route('/delete_reservation/<int:reservation_id>', methods=['POST'])
def delete_reservation(reservation_id):
    if 'usuario_id' not in session:
        flash('Debe iniciar sesión para eliminar reservas', 'warning')
        return redirect('/login')

    # Obtener la información de la reserva para redirigir a la misma fecha
    reserva = Reserva.get_by_id(reservation_id)
    fecha = None
    if reserva:
        fecha = reserva.fecha_reserva.strftime('%Y-%m-%d')

    # Verificar que el usuario sea el dueño de la reserva
    if reserva and reserva.id_usuario == session['usuario_id']:
        Reserva.delete(reservation_id)
        flash('Reserva eliminada con éxito', 'success')
    else:
        flash('No tienes permisos para eliminar esta reserva', 'danger')

    return redirect(url_for('reserva', selected_date=fecha) if fecha else url_for('reserva'))


@app.route('/mostrar_reservas')
def mostrar_reservas():
    if 'usuario_id' not in session:
        flash('Debe iniciar sesión para ver sus reservas', 'danger')
        return redirect('/login')

    # Mostrar solo las reservas del usuario actual
    user_id = session['usuario_id']
    user_reservas = Reserva.get_by_user_id(user_id)

    return render_template('mis_reservas.html', reservas=user_reservas)


@app.route('/api/disponibilidad/<string:fecha>/<int:cancha_id>')
def api_disponibilidad(fecha, cancha_id):
    """API para obtener disponibilidad de una cancha en una fecha específica"""
    if 'usuario_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        
        # Verificar que la cancha exista
        cancha = Cancha.get_by_id(cancha_id)
        if not cancha:
            return jsonify({'error': 'Cancha no encontrada'}), 404
            
        # Obtener reservas para esa fecha y cancha
        reservas_dia = Reserva.get_reservas_for_cancha_and_date(cancha_id, fecha_obj)
        
        # Crear un arreglo de disponibilidad para cada hora
        disponibilidad = []
        for hora in range(8, 23):  # Horario de 8am a 10pm
            disponible = hora not in reservas_dia
            
            # Si hay reserva, obtener información adicional
            info_reserva = None
            if not disponible:
                info_reserva = {
                    'usuario_id': reservas_dia[hora]['id_usuario'],
                    'usuario_nombre': reservas_dia[hora]['usuario_nombre'],
                    'es_propietario': reservas_dia[hora]['id_usuario'] == session['usuario_id']
                }
            
            disponibilidad.append({
                'hora': hora,
                'hora_formato': f"{hora:02d}:00",
                'disponible': disponible,
                'reserva': info_reserva
            })
            
        return jsonify({
            'fecha': fecha,
            'cancha_id': cancha_id,
            'cancha_nombre': cancha.nombre,
            'disponibilidad': disponibilidad
        })
        
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}), 400
    except Exception as e:
        logging.error(f"Error en api_disponibilidad: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500


@app.route('/calendario_mensual')
def calendario_mensual():
    if 'usuario_id' not in session:
        flash('Debe iniciar sesión para ver el calendario', 'warning')
        return redirect('/login')
        
    # Obtener mes y año desde los parámetros o usar el actual
    year = request.args.get('year', datetime.now().year)
    month = request.args.get('month', datetime.now().month)
    
    try:
        year = int(year)
        month = int(month)
        primer_dia = datetime(year, month, 1)
    except (ValueError, TypeError):
        primer_dia = datetime(datetime.now().year, datetime.now().month, 1)
        year = primer_dia.year
        month = primer_dia.month
    
    # Calcular mes anterior y siguiente
    if month == 1:
        mes_anterior = (year - 1, 12)
    else:
        mes_anterior = (year, month - 1)
        
    if month == 12:
        mes_siguiente = (year + 1, 1)
    else:
        mes_siguiente = (year, month + 1)
    
    # Obtener todas las reservas del mes para el usuario actual
    reservas_mensuales = Reserva.get_reservas_mensuales(session['usuario_id'], year, month)
    
    return render_template('calendario_mensual.html', 
                          year=year, 
                          month=month, 
                          primer_dia=primer_dia,
                          mes_anterior=mes_anterior,
                          mes_siguiente=mes_siguiente,
                          reservas=reservas_mensuales,
                          now=datetime.now())  # Pasar la fecha actual en lugar de timedelta
