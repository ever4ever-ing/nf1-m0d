from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        resultados = connectToMySQL('su_base_de_datos').query_db(query)
        usuarios = []
        for usuario in resultados:
            usuarios.append(cls(usuario))
        return usuarios

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO usuarios (nombre, email, password) 
        VALUES (%(nombre)s, %(email)s, %(password)s);
        """
        return connectToMySQL('pet').query_db(query, data)

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL('pet').query_db(query, {'email': email})
        if len(resultado) < 1:
            return False
        return cls(resultado[0])
    
    @staticmethod
    def validar_usuario(usuario):
        is_valid = True
        if len(usuario['nombre']) < 3:
            flash("El nombre debe tener al menos 3 caracteres.", "error")
            is_valid = False
        if not EMAIL_REGEX.match(usuario['email']):
            flash("Email inválido.", "error")
            is_valid = False
        if len(usuario['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "error")
            is_valid = False
        return is_valid