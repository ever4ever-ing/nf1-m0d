from flask import render_template, request, redirect, session, flash
from flask_app import app, bcrypt
from flask_app.models.usuario import Usuario
from flask_app.models.mascota import Mascota

# Aquí van todas las rutas y funciones de manejo (por ejemplo, index, registro, login, etc.)

@app.route("/registro_usuario")
def registro_usuario():
    return render_template("registro_usuario.html")

@app.route("/crear_usuario", methods=['POST'])
def crear_usuario():
    if not Usuario.validar_usuario(request.form):
        return redirect('/registro_usuario')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "nombre": request.form['nombre'],
        "email": request.form['email'],
        "password": pw_hash
    }
    usuario_id = Usuario.save(data)
    session['usuario_id'] = usuario_id
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = Usuario.get_by_email(request.form['email'])
        if usuario and bcrypt.check_password_hash(usuario.password, request.form['password']):
            session['usuario_id'] = usuario.id
            return redirect('/')
        flash("Email/Contraseña inválidos", "error")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route("/")
def index():
    if 'usuario_id' not in session: ## new
        return redirect('/login')   ## new
    mascotas = Mascota.get_by_usuario(session['usuario_id']) ##new
    
    if len(mascotas) == 0:
        flash("No tienes mascotas registradas Flash", "info")
    return render_template("index.html", todas_mascotas=mascotas)


