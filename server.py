from flask_app import app
from flask_app.controllers import usuarios, partidos, participantes, recintos, localidades, reservas, canchas, notificaciones

if __name__ == "__main__":
    app.run(debug=False, port=5000, host='0.0.0.0')
