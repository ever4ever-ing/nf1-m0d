from flask_app.config.dbconnection import connectToPostgreSQL
from flask import flash
import re
import os

from dotenv import load_dotenv
env_file = os.getenv('ENV_FILE', '.env')  # Por defecto, carga .env
load_dotenv(dotenv_path=env_file)

# Asegurarse de que las variables de entorno estén configuradas
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DATABASE')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NOMBRE_REGEX = re.compile(r'^[a-zA-Z\s]+$')


class Usuario:
    def __init__(self, data):
        self.id_usuario = data['id_usuario']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        resultados = connectToPostgreSQL(DATABASE).query_db(query)
        usuarios = []
        for usuario in resultados:
            usuarios.append(cls(usuario))
        return usuarios

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO usuarios (nombre, apellido, email, password) 
        VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s) RETURNING id_usuario;
        """
        return connectToPostgreSQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToPostgreSQL(DATABASE).query_db(query, {'email': email})
        if not resultado:  # Verifica si el resultado es None o False
            return False
        if len(resultado) < 1:  # Si es una lista vacía
            return False
        return cls(resultado[0])

    @classmethod
    def get_by_id(cls, id_usuario):
        query = "SELECT * FROM usuarios WHERE id = %(id_usuario)s;"
        resultado = connectToPostgreSQL(DATABASE).query_db(
            query, {'id_usuario': id_usuario})
        if not resultado:
            return None  # Cambiado de False a None para mayor consistencia
        return cls(resultado[0])

    @staticmethod
    def validar_usuario(usuario):
        is_valid = True

        # Verificar que 'usuario' sea un diccionario válido
        if not isinstance(usuario, dict):
            flash("Datos de usuario inválidos.", "error")
            return False

        if 'name' not in usuario or len(usuario['name']) < 3:
            flash("El nombre debe tener al menos 3 caracteres.", "error")
            is_valid = False
        if 'email' not in usuario or not EMAIL_REGEX.match(usuario['email']):
            flash("Email inválido.", "error")
            is_valid = False
        if 'password' not in usuario or len(usuario['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "error")
            is_valid = False

        return is_valid

    @staticmethod
    def validar_login(usuario):
        is_valid = True

        # Validación del email
        if not usuario['email'].strip():
            flash("El email es obligatorio.", "error")
            is_valid = False
        elif not EMAIL_REGEX.match(usuario['email']):
            flash("Por favor ingresa un email válido.", "error")
            is_valid = False

        # Validación de la contraseña
        if not usuario['password'].strip():
            flash("La contraseña es obligatoria.", "error")
            is_valid = False

        return is_valid
