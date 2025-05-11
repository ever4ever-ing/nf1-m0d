from flask import render_template, request, redirect, session, flash
from flask_app import app, bcrypt
from flask_app.models.usuario import Usuario
from flask_app.models.partido import Partido
from flask_app.models.localidad import Localidad
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
    return render_template("index.html")


@app.route("/dashboard")
@login_required
def dashboard():
    def agregar_participantes(lista_partidos):
        """Agrega los participantes a una lista de partidos"""
        if not lista_partidos:
            return []
        for partido in lista_partidos:
            partido.participantes = Partido.obtener_participantes(partido.id_partido)
        return lista_partidos
    
    # Obtener partidos organizados por el usuario actual
    mis_partidos = agregar_participantes(
        Partido.obtener_por_organizador(session['usuario_id'])
    )
    # Cargar las localidades para el renderizado
    localidades = Localidad.get_all()
      # Obtener partidos según filtro o disponibilidad
    id_localidad = request.args.get('id_localidad', type=int, default=0)
    
    # Utilizamos get_partidos_by_localidad tanto para todos como para un filtro específico
    # Este método ya maneja correctamente el caso de id_localidad = 0
    print(f"Filtrando partidos por localidad ID: {id_localidad}")
    partidos_filtrados = Partido.get_partidos_by_localidad(id_localidad)
    partidos = agregar_participantes(partidos_filtrados)
        
    return render_template(
        "dashboard.html",
        mis_partidos=mis_partidos,
        partidos=partidos,
        localidades=localidades,
        id_localidad=id_localidad,
        usuario_id=session['usuario_id']
    )



@app.route('/register', methods=['POST'])
def crear_usuario():
    if not Usuario.validar_usuario(request.form):
        return redirect('/registro_usuario')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'nombre': request.form['name'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'password': pw_hash
    }
    usuario_id = Usuario.save(data)
    session['usuario_id'] = usuario_id
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = Usuario.get_by_email(request.form['loginEmail'])
        if usuario and bcrypt.check_password_hash(usuario.password, request.form['loginPassword']):
            session['usuario_id'] = usuario.id_usuario
            return redirect('/dashboard')
        flash("Email/Contraseña inválidos", "error")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

