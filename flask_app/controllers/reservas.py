from flask import render_template, redirect, url_for, flash, jsonify, request, session
from flask_app.models.cancha import Cancha
from flask_app.models.reserva import Reserva
from flask_app import app
from datetime import datetime, date
import logging


@app.route('/reservar/<int:id_cancha>', methods=['GET', 'POST'])
def reservar(id_cancha):
    if 'usuario_id' not in session:
        flash('Debe iniciar sesión para realizar una reserva', 'warning')
        return redirect('/login')

    if request.method == 'POST':
        # Obtener datos del formulario
        fecha_reserva = request.form.get('fecha_reserva')
        hora_inicio = request.form.get('hora_inicio')
        hora_fin = request.form.get('hora_fin')

        # Validar los datos de la reserva
        datos_reserva = {
            'id_cancha': id_cancha,
            'id_usuario': session['usuario_id'],
            'fecha_reserva': fecha_reserva,
            'hora_inicio': hora_inicio,
            'hora_fin': hora_fin
        }

        if Reserva.validar_reserva(datos_reserva):
            Reserva.guardar(datos_reserva)
            flash('Reserva realizada con éxito', 'success')
            return redirect(url_for('dashboard'))

    return render_template('dashboard.html', id_cancha=id_cancha)


@app.route('/mostrar_disponibilidad')
def mostrar_disponibilidad():
    if 'usuario_id' not in session:
        flash('Debe iniciar sesión para ver las reservas', 'warning')
        return redirect('/login')

    # Obtener la fecha seleccionada desde los parámetros de la URL
    fecha_seleccionada = request.args.get(
        'selected_date', datetime.now().date().strftime('%Y-%m-%d'))
    try:
        fecha_seleccionada = datetime.strptime(
            fecha_seleccionada, '%Y-%m-%d').date()
    except ValueError:
        fecha_seleccionada = datetime.now().date()

    # Obtener el ID del recinto desde los parámetros de la URL
    id_recinto = request.args.get('id_recinto')
    if not id_recinto:
        flash('ID de recinto no proporcionado', 'danger')
        return redirect('/')

    # Llamar al método para obtener las reservas por fecha y recinto
    reservas = Reserva.obtener_por_recinto( id_recinto)

    # Generar disponibilidad por hora si no hay reservas

    return render_template('agenda.html',
                           reservas=reservas,
                           fecha_seleccionada=fecha_seleccionada,
                           id_recinto=id_recinto)


@app.route('/eliminar_reserva/<int:id_reserva>', methods=['POST'])
def eliminar_reserva(id_reserva):
    if 'usuario_id' not in session:
        flash('Debe iniciar sesión para eliminar reservas', 'warning')
        return redirect('/login')

    # Obtener la información de la reserva para redirigir a la misma fecha
    reserva = Reserva.obtener_por_id(id_reserva)
    fecha = None
    if reserva:
        fecha = reserva.fecha_reserva.strftime('%Y-%m-%d')

    # Verificar que el usuario sea el dueño de la reserva
    if reserva and reserva.id_usuario == session['usuario_id']:
        Reserva.eliminar(id_reserva)
        flash('Reserva eliminada con éxito', 'success')
    else:
        flash('No tienes permisos para eliminar esta reserva', 'danger')

    return redirect(url_for('reservas', selected_date=fecha) if fecha else url_for('reservas'))


@app.route('/mostrar_reservas')
def mostrar_reservas():
    if 'usuario_id' not in session:
        flash('Debe iniciar sesión para ver sus reservas', 'danger')
        return redirect('/login')

    # Mostrar solo las reservas del usuario actual
    id_usuario = session['usuario_id']
    reservas_usuario = Reserva.obtener_por_usuario(id_usuario)

    return render_template('agenda.html', reservas=reservas_usuario)


@app.route('/api/disponibilidad/<string:fecha>/<int:id_cancha>')
def api_disponibilidad(fecha, id_cancha):
    """API para obtener disponibilidad de una cancha en una fecha específica"""
    if 'usuario_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    try:
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()

        # Verificar que la cancha exista
        cancha = Cancha.obtener_por_id(id_cancha)
        if not cancha:
            return jsonify({'error': 'Cancha no encontrada'}), 404

        # Obtener reservas para esa fecha y cancha
        reservas_dia = Reserva.obtener_reservas_por_cancha_y_fecha(
            id_cancha, fecha_obj)

        # Crear un arreglo de disponibilidad para cada hora
        disponibilidad = []
        for hora in range(8, 23):  # Horario de 8am a 10pm
            disponible = hora not in reservas_dia

            # Si hay reserva, obtener información adicional
            info_reserva = None
            if not disponible:
                info_reserva = {
                    'id_usuario': reservas_dia[hora]['id_usuario'],
                    'nombre_usuario': reservas_dia[hora]['usuario_nombre'],
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
            'id_cancha': id_cancha,
            'nombre_cancha': cancha.nombre,
            'disponibilidad': disponibilidad
        })

    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}), 400
    except Exception as e:
        logging.error(f"Error en api_disponibilidad: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500


