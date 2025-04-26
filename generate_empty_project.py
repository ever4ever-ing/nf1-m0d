import os

# Estructura del proyecto
project_structure = {
    "flask_app": {
        "__init__.py": "",
        "config": {
            "dbconnection.py": "",
            "config.env": "",
            "setup_nginx.sh": "",
            "setup_gunicorn.sh": ""
        },
        "controllers": {
            "usuarios.py": "",

        },
        "models": {
            "usuario.py": "",
        },
        "templates": {
            "index.html": "",
            "dashboard.html": "",
            "login.html": "",
            "nuevo.html": "",
            "editar_partido.html": "",
            "registrar_recinto.html": "",
            "ver_partido.html": ""
        },
        "static": {
            "css": {
                "style.css": ""
            },
            "js": {
                "script.js": ""
            }
        },
        "bd": {
            "bd.sql": "",
            "create_tables.py": ""
        },
        "todo.md": ""
    },
    "wsgi.py": "",
    "server.py": "",
    "requirements.txt": "",
    "Readme.md": "",
    ".gitignore": ""
}

# Función para crear carpetas y archivos
def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):  # Es una carpeta
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:  # Es un archivo
            with open(path, "w", encoding="utf-8") as file:
                file.write(content)

# Crear la estructura del proyecto
base_path = os.getcwd()  # Obtener el directorio actual
create_structure(base_path, project_structure)
