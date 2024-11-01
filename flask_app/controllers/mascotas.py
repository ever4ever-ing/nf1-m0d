from flask import render_template, request, redirect, session, flash
from flask_app import app, bcrypt
from flask_app.models.usuario import Usuario
from flask_app.models.mascota import Mascota


@app.route("/crear_mascota", methods=['POST'])
def crear_mascota():
    datos = {
        "nombre": request.form['nombre'],
        "tipo": request.form['tipo'],
        "color": request.form['color'],
        "usuario_id": session['usuario_id']  # Añade el usuario_id desde la sesión
    }

    if not Mascota.validar_mascota(datos):
        flash("El nombre debe tener al menos 3 caracteres", "error")
        return redirect('/')
    Mascota.save(datos)
    return redirect('/')

@app.route("/editar_mascota/<int:id>")
def editar_mascota(id):
    if 'usuario_id' not in session:
        return redirect('/login')
    mascota = Mascota.get_by_id(id)
    if mascota.usuario_id != session['usuario_id']:
        flash("No tienes permiso para editar esta mascota", "error")
        return redirect('/')
    return render_template("editar_mascota.html", mascota=mascota)

@app.route("/actualizar_mascota", methods=['POST'])
def actualizar_mascota():
    if 'usuario_id' not in session:
        return redirect('/login')
    datos = {
        "id": request.form['id'],
        "nombre": request.form['nombre'],
        "tipo": request.form['tipo'],
        "color": request.form['color']
    }
    
    Mascota.update(datos)
    flash("Mascota actualizada exitosamente", "success")
    return redirect('/')

@app.route("/eliminar_mascota/<int:id>")
def eliminar_mascota(id):
    if 'usuario_id' not in session:
        return redirect('/login')
    mascota = Mascota.get_by_id(id)
    if mascota.usuario_id != session['usuario_id']:
        flash("No tienes permiso para eliminar esta mascota", "error")
        return redirect('/')
    Mascota.delete(id)
    flash("Mascota eliminada exitosamente", "success")
    return redirect('/')

### Se cambio nombre
@app.route("/registrar_mascota")
def registrar_mascota():
    return render_template("registrar_mascota.html")

