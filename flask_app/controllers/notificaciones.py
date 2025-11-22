from flask import render_template, redirect, session, jsonify, request
from flask_app import app
from flask_app.models.notificacion import Notificacion
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/notificaciones')
@login_required
def ver_notificaciones():
    """Página de notificaciones"""
    notificaciones = Notificacion.obtener_por_usuario(session['usuario_id'])
    return render_template('notificaciones.html', notificaciones=notificaciones)

@app.route('/notificaciones/contar')
@login_required
def contar_notificaciones():
    """API para contar notificaciones no leídas"""
    total = Notificacion.contar_no_leidas(session['usuario_id'])
    return jsonify({'total': total})

@app.route('/notificaciones/marcar_leida/<int:id>', methods=['POST'])
@login_required
def marcar_notificacion_leida(id):
    """Marca una notificación como leída"""
    Notificacion.marcar_como_leida(id)
    return jsonify({'success': True})

@app.route('/notificaciones/marcar_todas_leidas', methods=['POST'])
@login_required
def marcar_todas_leidas():
    """Marca todas las notificaciones como leídas"""
    Notificacion.marcar_todas_leidas(session['usuario_id'])
    return jsonify({'success': True})

@app.route('/notificaciones/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_notificacion(id):
    """Elimina una notificación"""
    Notificacion.eliminar(id)
    return jsonify({'success': True})
