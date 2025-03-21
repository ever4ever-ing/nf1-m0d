from flask import render_template, request, redirect, session, flash
from flask_app import app, bcrypt
from flask_app.models.usuario import Usuario
from flask_app.models.partido import Partido
from datetime import date
from functools import wraps

# Decorator para verificar sesión

# Decorador para verificar si el usuario está logueado
def login_required(f):
    @wraps(f) # Esto es para que la función decorada mantenga su nombre
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

# Rutas de la aplicación


@app.route("/")
def index():
    Usuarios = Usuario.get_all()
    if not Usuarios:  # Verifica si la lista está vacía
        print("No hay usuarios registrados.")
    else:
        print("Usuarios:", Usuarios)
    return render_template("index.html")


@app.route("/dashboard")
@login_required
def dashboard():
    mis_partidos = Partido.obtener_por_organizador(session['usuario_id'])
    for partido in mis_partidos:
        partido.participantes = Partido.obtener_participantes(partido.id_partido)
    
    print("user id", session['usuario_id'])
    partidos = Partido.get_match_disponibles(session['usuario_id'])
    for partido in partidos:
        partido.participantes = Partido.obtener_participantes(partido.id_partido)

    return render_template(
        "dashboard.html",
        mis_partidos=mis_partidos,
        partidos=partidos,
        usuario_id=session['usuario_id']
    )


@app.route('/register', methods=['POST'])
def crear_usuario():
    if not Usuario.validar_usuario(request.form):
        return redirect('/registro_usuario')

    #pw_hash = bcrypt.generate_password_hash(request.form['password'])
    pw_hash = request.form['password']
    data = {
        'nombre': request.form['name'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'password': pw_hash
    }
    usuario_id = Usuario.save(data)
    if not usuario_id:
        flash("No se pudo crear el usuario.", "error")
        return redirect('/')
    else:
        print("Usuario creado con ID:", usuario_id)
        session['usuario_id'] = usuario_id
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Validar que los campos no estén vacíos
        email = request.form['loginEmail'].strip()
        password = request.form['loginPassword'].strip()

        if not email or not password:
            flash("Todos los campos son obligatorios.", "error")
            return render_template("index.html")

        # Buscar usuario por email
        usuario = Usuario.get_by_email(email)
        print(usuario)
        if not usuario:
            print("Usuario no encontrado")
            flash("Usuario no encontrado.", "error")
            return render_template("index.html")

        # Comparar contraseñas directamente
        if usuario.password != password:
            print("Contraseña incorrecta")
            flash("Credenciales inválidas.", "error")
            return render_template("index.html")

        # Iniciar sesión
        session['usuario_id'] = usuario.id_usuario
        return redirect('/dashboard')

    return render_template("index.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

