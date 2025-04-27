from flask import render_template, redirect, request, flash, session, url_for
from flask_app.models.participante import Participante
from flask_app.models.partido import Partido
from flask_app.models.usuario import Usuario
from flask_app.models.recinto import Recinto
from datetime import datetime
from flask_app import app
from flask_app.models.recinto import Recinto
from flask_app.models.localidad import Localidad
from functools import wraps
import logging

# Configuración básica del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Decorador para verificar si el usuario está logueado
def login_required(f):
    @wraps(f) # Esto es para que la función decorada mantenga su nombre
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

# Rutas de la aplicación


@app.route("/recintos", methods=["GET", "POST"])
@login_required
def recintos():
    Recintos = Recinto.get_all()
    Localidades = Localidad.get_all()
    logging.debug(f"Recintos: {Recintos}")
    if not Recintos:  # Verifica si la lista está vacía
        logging.debug("No hay recintos registrados.")
    else:
        logging.debug(f"Recintos: {Recinto}")
    return render_template("registrar_recinto.html", recintos=Recintos, localidades=Localidades)

@app.route("/recintos/registrar", methods=["POST"])
@login_required
def registrar_recinto():
    required_fields = ['nombre', 'direccion', 'id_localidad']
    missing_fields = [field for field in required_fields if field not in request.form]

    if missing_fields:
        flash(f"Faltan los siguientes campos obligatorios: {', '.join(missing_fields)}", "error")
        return redirect("/recintos")
    data = {
        'nombre': request.form['nombre'],
        'direccion': request.form['direccion'],
        'id_localidad': request.form['id_localidad']
    }
    logging.info(f"Datos enviados para guardar recinto: {data}")
    resultado = Recinto.registrar_recinto(data)
    if resultado:
        flash("Recinto registrado correctamente.", "success")
        return redirect("/recintos")
    else:
        flash("Error al registrar el recinto. Por favor, inténtelo de nuevo.", "error")
        return redirect("/recintos")
    

@app.route('/agendar_recinto/<int:id_recinto>', methods=['GET'])
@login_required
def agendar_recinto(id_recinto):
        recinto = Recinto.obtener_por_id(id_recinto)
        if recinto:
            return render_template("agenda.html")