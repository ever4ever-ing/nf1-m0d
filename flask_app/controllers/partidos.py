# controladores/viajes.py
from flask import render_template, redirect, request, flash, session, url_for
from flask_app.models.localidad import Localidad
from flask_app.models.participante import Participante
from flask_app.models.partido import Partido
from flask_app.models.recinto import Recinto
from flask_app.models.usuario import Usuario
from datetime import datetime
from flask_app import app




@app.route('/nuevo_partido', methods=['GET', 'POST'])
def nuevo_partido():
    if request.method == 'GET':
        # Verificar si el usuario está logueado
        localidades = Localidad.get_all()
        return render_template('nuevo.html', localidades=localidades)
    
    if request.method == 'POST':
        # Crear diccionario con los datos del formulario
        data = {
            'id_organizador': session['usuario_id'],
            'id_localidad': request.form['id_localidad'],
            'fecha_inicio': request.form['fechaInicio'],
            'descripcion': request.form['descripcion'],
        }

        # Validar los datos
        errores = Partido.validar_partido(data)
        if errores:
            for error in errores:
                flash(error, 'error')
            return render_template('nuevo.html', data=data)
        # Crear el partido
        partido_id = Partido.crear(data)

        print("Partido creado con ID:", partido_id)
        if partido_id:
            flash('Partido creado exitosamente', 'success')
            return redirect(url_for('editar_partido', id=partido_id ))
        else:
            flash('Error al crear el partido', 'error')
            return render_template('nuevo.html', data=data)

@app.route('/ver_partido/<int:id>')
def ver_partido(id):
    partido = Partido.obtener_por_id(id)
    if not partido:
        flash("Partido no encontrado.", "error")
        return redirect(url_for('dashboard'))
        
    participantes = Participante.obtener_participantes_por_partido(id)
    
    ya_unido = False
    if 'usuario_id' in session:
        ya_unido = any(p['id_usuario'] == session['usuario_id'] for p in participantes)
    
    # Obtener nombre del organizador
    organizador = Usuario.get_by_id(partido.id_organizador)
    partido.organizador_nombre = organizador.nombre if organizador else "Desconocido"

    # Obtener información de la reserva si existe
    if partido.id_reserva:
        # Aquí deberías tener lógica para obtener los detalles de la reserva
        # y asignarlos a partido.reserva_info como se discutió anteriormente.
        # Por ejemplo:
        # reserva_obj = Reserva.obtener_detalles_completos(partido.id_reserva)
        # partido.reserva_info = reserva_obj 
        pass # Placeholder para la lógica de reserva_info

    # Lógica para invitados (si la tienes)
    invitados = [] # Reemplaza con tu lógica para obtener invitados

    return render_template(
        'ver_partido.html', 
        partido=partido, 
        participantes=participantes,
        invitados=invitados, # Pasa la lista de invitados
        ya_unido=ya_unido   # Pasa el estado de si el usuario ya está unido
    )

@app.route('/eliminar_partido/<int:id>')
def eliminar_partido(id):
    if Partido.eliminar(id):
        flash('partido eliminado exitosamente', 'success')
    else:
        flash('Error al eliminar el partido', 'error')
    return redirect(url_for('dashboard'))


@app.route("/editar_partido/<int:id>")
def editar_partido(id):
    if 'usuario_id' not in session:
        return redirect('/login')
    
    partido = Partido.obtener_por_id(id)
    if partido.id_organizador != session['usuario_id']:
        flash("No tienes permiso para editar este partido", "error") 
        return redirect(url_for('dashboard'))
    else:
        recintos = Recinto.obtener_por_id_localidad(partido.id_localidad)
        ##mostrar usuarios que no esten en el partido solamente
        return render_template("editar_partido.html", partido=partido, usuarios=Usuario.get_all(), participantes=Participante.obtener_participantes_por_partido(id),recintos=recintos)
    
@app.route("/actualizar_partido", methods=['POST'])
def actualizar_partido():
    if 'usuario_id' not in session:
        return redirect('/login')
    
    datos = {
        "id_partido": request.form['id'],
        'id_localidad': request.form['id_localidad'],
        "fecha_inicio": request.form['fechaInicio'],
        "descripcion": request.form['descripcion'],
        "participantes": Participante.obtener_participantes_por_partido(request.form['id'])
    }
    print("********ACTUALIZANDO********")
    print("Lista de participantes", datos['participantes'])
    Partido.actualizar(datos)
    
    flash("partido actualizado exitosamente", "success")
    return redirect(url_for('dashboard'))

@app.route('/partido/<int:id_partido>/unirse', methods=['POST'])
def unirse_partido(id_partido):
    if 'usuario_id' not in session:
        flash("Debes iniciar sesión para unirte a un partido.", "warning")
        return redirect(url_for('login')) # O a donde quieras redirigir si no está logueado

    # Verificar que el partido exista
    partido_existente = Partido.obtener_por_id(id_partido)
    if not partido_existente:
        flash("El partido al que intentas unirte no existe.", "error")
        return redirect(url_for('dashboard'))

    # Datos para crear el participante
    datos_participante = {
        'id_partido': id_partido,
        'id_usuario': session['usuario_id']
        # Puedes añadir más campos si tu tabla 'participantes_partido' los requiere,
        # como 'estado_confirmacion', 'fecha_union', etc.
    }

    # Verificar si el usuario ya está unido (opcional, pero buena práctica)
    # Esto dependerá de cómo tengas implementado Participante.obtener_participantes_por_partido
    # o si tienes un método específico como Participante.ya_es_participante(datos_participante)
    
    # Ejemplo de verificación (necesitarás adaptar esto a tus modelos):
    participantes_actuales = Participante.obtener_participantes_por_partido(id_partido)
    if any(p['id_usuario'] == session['usuario_id'] for p in participantes_actuales):
        flash("Ya estás unido a este partido.", "info")
        return redirect(url_for('ver_partido', id=id_partido))

    # Intentar agregar al participante
    # Asumiendo que tienes un método Participante.agregar(datos) o similar
    if Participante.agregar(datos_participante): # Necesitarás crear este método en tu modelo Participante
        flash("¡Te has unido al partido exitosamente!", "success")
    else:
        flash("Hubo un error al intentar unirte al partido.", "error")

    return redirect(url_for('ver_partido', id=id_partido))

@app.route('/partido/<int:id_partido>/salir', methods=['POST'])
def salir_partido(id_partido):
    if 'usuario_id' not in session:
        flash("Debes iniciar sesión.", "warning")
        return redirect(url_for('login'))

    datos_eliminar = {
        'id_partido': id_partido,
        'id_usuario': session['usuario_id']
    }

    # Asumiendo que tienes un método Participante.eliminar_participacion(datos)
    if Participante.eliminar_participacion(datos_eliminar): # Necesitarás crear este método
        flash("Has salido del partido.", "success")
    else:
        flash("Error al intentar salir del partido.", "error")
    
    return redirect(url_for('ver_partido', id=id_partido))
    
    """
    
@app.route('/editar_viaje/<int:id>', methods=['GET', 'POST'])
def editar_viaje(id):
    viaje = Viaje.obtener_por_id(id)
    if not viaje:
        flash('Viaje no encontrado', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        data = {
            'id_viaje': id,
            'destino': request.form['destino'],
            'fecha_inicio': request.form['fechaInicio'],
            'fecha_fin': request.form['fechaFin'],
            'itinerario': request.form['itinerario'],
        }
        errores = Viaje.validar_viaje(data)
        if errores:
            for error in errores:
                flash(error, 'error')
            return render_template('editar_viaje.html', viaje=data)

        if Viaje.actualizar(data):
            flash('Viaje actualizado exitosamente', 'success')
            print(f"Viaje con ID {id} actualizado correctamente")  # Mensaje en consola
            return redirect(url_for('dashboard'))  # Redirigir a la ruta principal
        
        flash('Error al actualizar el viaje', 'error')
        return render_template('editar_viaje.html', viaje=data)

    return render_template('editar_viaje.html', viaje=viaje)

    """