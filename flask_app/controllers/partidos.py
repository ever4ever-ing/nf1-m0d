# controladores/viajes.py
from flask import render_template, redirect, request, flash, session, url_for
from flask_app.models.participante import Participante
from flask_app.models.partido import Partido
from flask_app.models.usuario import Usuario
from datetime import datetime
from flask_app import app




@app.route('/nuevo_partido', methods=['GET', 'POST'])
def nuevo_partido():
    if request.method == 'GET':
        return render_template('nuevo.html')
    
    if request.method == 'POST':
        # Crear diccionario con los datos del formulario
        data = {
            'id_organizador': session['usuario_id'],
            'lugar': request.form['lugar'],
            'fecha_inicio': request.form['fechaInicio'],
            'descripcion': request.form['descripcion'],
        }
        log = f"Datos del formulario: {data}"
        print(log)
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
            flash('partido creado exitosamente', 'success')
            return redirect(url_for('dashboard'))
        
        flash('Error al crear el partido', 'error')
        return render_template('nuevo.html', data=data)

@app.route('/ver_partido/<int:id>')
def ver_partido(id):
    partido = Partido.obtener_por_id(id)
    print("Controlador")
    print("id:",id)
    print("partido:",partido)
    participantes = Participante.obtener_participantes_por_partido(id)
    usuario_en_partido = any(participante['id_usuario'] == session['usuario_id'] for participante in participantes)
    if usuario_en_partido:
        print("Usuario ya esta en el partido")
        ready = True
    else:
        print("Usuario no esta en el partido")
        ready = False
    
    return render_template('ver_partido.html', partido=partido, participantes=participantes, usuario_id=session['usuario_id'],ready=ready)

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
        ##mostrar usuarios que no esten en el partido solamente
        return render_template("editar_partido.html", partido=partido, usuarios=Usuario.get_all(), participantes=Participante.obtener_participantes_por_partido(id))
    
@app.route("/actualizar_partido", methods=['POST'])
def actualizar_partido():
    if 'usuario_id' not in session:
        return redirect('/login')
    
    datos = {
        "id_partido": request.form['id'],
        "lugar": request.form['lugar'],
        "fecha_inicio": request.form['fechaInicio'],
        "descripcion": request.form['descripcion'],
        "participantes": Participante.obtener_participantes_por_partido(request.form['id'])
    }
    print("********ACTUALIZANDO********")
    print("Lista de participantes", datos['participantes'])
    Partido.actualizar(datos)
    
    flash("partido actualizado exitosamente", "success")
    return redirect(url_for('dashboard'))


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