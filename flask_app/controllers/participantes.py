from flask import flash, render_template, request, redirect, url_for, session
from flask_app import app
from flask_app.models.participante import Participante
from flask_app.models.notificacion import Notificacion
from flask_app.models.usuario import Usuario


@app.route('/agregar_participante', methods=['POST'])
def agregar_participante():
    data = {
        'id_partido': request.form['id_partido'],
        'id_usuario': request.form['id_usuario']
    }
    
    # Verificar si el usuario ya está en el partido
    if Participante.verificar_participante(data['id_partido'], data['id_usuario']):
        flash("Este usuario ya está en el partido", "warning")
        return redirect(url_for('editar_partido', id=data['id_partido']))
    
    #print("Datos del formulario para AGREGAR PARTICIPANTE:", data)
    Participante.agregar_participante(data)
    
    # Crear notificación
    usuario = Usuario.get_by_id(data['id_usuario'])
    if usuario:
        Notificacion.notificar_union_partido(
            data['id_partido'], 
            data['id_usuario'], 
            usuario.nombre
        )
    
    flash("Participante agregado exitosamente", "success")
    return redirect(url_for('editar_partido', id=data['id_partido']))

@app.route('/eliminar_participante', methods=['POST'])
def eliminar_participante():
    data = {
        'id_partido': request.form['id_partido_delete'], 
        'id_usuario': request.form['id_usuario_delete']
    }
    #print("Datos del formulario para ELIMINAR:", data)
    
    # Obtener info del usuario antes de eliminarlo
    usuario = Usuario.get_by_id(data['id_usuario'])
    
    Participante.eliminar_participante(data)
    
    # Crear notificación de salida
    if usuario:
        Notificacion.notificar_salida_partido(
            data['id_partido'], 
            data['id_usuario'], 
            usuario.nombre
        )
    
    return redirect(url_for('editar_partido', id=data['id_partido']))

@app.route('/unirse', methods=['POST'])
def unirse():
    data = {
        'id_partido': request.form['id_partido'],
        'id_usuario': request.form['id_usuario']
    }
    
    # Verificar si el usuario ya está en el partido
    if Participante.verificar_participante(data['id_partido'], data['id_usuario']):
        flash("Ya estás unido a este partido", "info")
        return redirect(url_for('dashboard'))
    
    #print("Datos del formulario para UNIRSE:", data)
    Participante.agregar_participante(data)
    
    # Crear notificación
    usuario = Usuario.get_by_id(data['id_usuario'])
    if usuario:
        Notificacion.notificar_union_partido(
            data['id_partido'], 
            data['id_usuario'], 
            usuario.nombre
        )
    
    flash("Te has unido al partido", "success")
    return redirect(url_for('dashboard'))
    

