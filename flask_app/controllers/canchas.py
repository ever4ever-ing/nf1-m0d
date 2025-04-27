from flask import render_template, redirect, request, flash, session
from flask_app.models.cancha import Cancha
from flask_app import app

@app.route('/canchas')
def mostrar_canchas():
    if 'usuario_id' not in session:
        return redirect('/login')
    canchas = Cancha.get_all()
    return render_template('canchas.html', canchas=canchas)

@app.route('/canchas/nueva', methods=['GET', 'POST'])
def registrar_cancha():
    if 'usuario_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        data = {
            'nombre': request.form['nombre_cancha'],
            'id_recinto': request.form['id_recinto']
        }
        Cancha.save(data)
        flash('Cancha registrada con éxito', 'success')
        return redirect('/recintos')
    