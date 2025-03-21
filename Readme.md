# Readme:

## Instalación




Crear un entorno virtual con el siguiente comando:
`python3 -m venv venv` 

Activar el entorno virtual con el siguiente comando:
`source venv/bin/activate`

Para instalar las dependencias del proyecto, se puede utilizar `pip` o `pipenv`:
`pip install -r requirements.txt`


sudo rm /etc/nginx/sites-enabled/default
sudo service nginx restart
sudo chmod 755 /home/ubuntu

## Configuración de la base de datos

comandos: 

    sudo apt-get update
    sudo apt-get install mysql-server
    sudo apt-get update
    sudo mysql -uroot -p
    sudo mysql_secure_installation
    sudo mysql -u root -p
    sudo apt-get update
    sudo apt-get install python3-pip nginx git -y
    sudo apt-get install python3-venv -y
## Estructura del proyecto


## Produccion
gunicorn --bind 0.0.0.0:5000 wsgi:application

## Estructura del proyecto
Friendship-Flask/ 

    ├── flask_app/  
    │   ├── \_\_init\_\_.py  
    │   ├── config/ 
    │   │   └── mysqlconnection.py  
    │   ├── controllers/  
    │   │   └── usuarios.py  
    │   ├── models/  
    │   │   ├── usuario.py  
    │   ├── static/  
    │   │   ├── css/  
    │   │   │   └── style.css  
    │   │   └── js/  
    │   │       └── script.js  
    │   ├── templates/  
    │   │   └── index.html  
    │   └── bd/  
    │       └── bd.sql  
    │  
    ├── .gitignore  
    ├── requirements.txt  
    ├── server.py  
    └── README.md


## Explicación

- `flask_app/`: Contiene la aplicación Flask.
- `__init__.py`: Inicializa la aplicación Flask.
- `config/`: Archivos de configuración, como la conexión a la base de datos.
- `controllers/`: Controladores que manejan las rutas y la lógica de la aplicación.
- `models/`: Modelos que representan las entidades de la base de datos.
- `static/`: Archivos estáticos como CSS y JavaScript.
- `templates/`: Plantillas HTML para la aplicación.
- `bd/`: Archivos relacionados con la base de datos, como scripts SQL.
- `.gitignore`: Archivos y directorios que Git debe ignorar.
- `requirements.txt`: Lista de dependencias de Python necesarias para el proyecto.
- `server.py`: Archivo principal para ejecutar la aplicación Flask.
- `Readme.md`: Documentación del proyecto.