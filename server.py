from flask_app import app
from flask_app.controllers import usuarios, partidos, participantes

if __name__ == "__main__":
    
    app.run(debug=True, port=5000, host='0.0.0.0')
