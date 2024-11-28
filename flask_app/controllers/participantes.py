from flask import render_template, request, redirect, url_for
from flask_app import app
from flask_app.models.participante import Participante


@app.route('/agregar_participante', methods=['POST'])
def agregar_participante():
    data = {
        'id_partido': request.form['id_partido'],
        'id_usuario': request.form['id_usuario']
    }
    print("Datos del formulario para AGREGAR PARTICIPANTE:", data)
    Participante.agregar_participante(data)
    return redirect(url_for('editar_partido', id=data['id_partido']))

@app.route('/eliminar_participante', methods=['POST'])
def eliminar_participante():
    data = {
        'id_partido': request.form['id_partido_delete'], 
        'id_usuario': request.form['id_usuario_delete']
    }
    print("Datos del formulario para ELIMINAR:", data)
    Participante.eliminar_participante(data)
    return redirect(url_for('editar_partido', id=data['id_partido']))
    

