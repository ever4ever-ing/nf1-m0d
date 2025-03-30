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

@app.route("/localidades", methods=["GET", "POST"])
@login_required
def get_localidades():
    
    localidades = Localidad.get_all()
    if not localidades:  # Verifica si la lista está vacía
        logging.info("No hay localidades registradas.")
    else:
        logging.info(f"Localidades: {localidades}")
    return localidades

