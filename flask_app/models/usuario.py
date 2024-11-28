from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NOMBRE_REGEX = re.compile(r'^[a-zA-Z\s]+$')
DATABASE = 'nosfalta1'

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
        resultados = connectToMySQL(DATABASE).query_db(query)
        usuarios = []
        for usuario in resultados:
            usuarios.append(cls(usuario))
        return usuarios

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO usuarios (nombre, apellido, email, password) 
        VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL(DATABASE).query_db(query, {'email': email})
        if len(resultado) < 1:
            return False
        return cls(resultado[0])

    @classmethod
    def get_by_id(cls, id_usuario):
        query = "SELECT * FROM usuarios WHERE id = %(id_usuario)s;"
        resultado = connectToMySQL(DATABASE).query_db(query, {'id': id})
        if len(resultado) < 1:
            return False
        return cls(resultado[0])

    @staticmethod
    def validar_usuario(usuario):
        is_valid = True
        if len(usuario['name']) < 3:
            flash("El nombre debe tener al menos 3 caracteres.", "error")
            is_valid = False
        if not EMAIL_REGEX.match(usuario['email']):
            flash("Email inválido.", "error")
            is_valid = False
        if len(usuario['password']) < 8:
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