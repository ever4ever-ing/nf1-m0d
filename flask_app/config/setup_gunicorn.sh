#!/bin/bash

# Cargar configuraciones desde config.env
CONFIG_FILE="config.env"
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
else
    echo "Archivo $CONFIG_FILE no encontrado. Por favor, crea el archivo con las configuraciones necesarias."
    exit 1
fi

# Validar que las variables requeridas estén definidas
if [[ -z "$PROJECT_NAME" || -z "$REPO_NAME" || -z "$SERVER_USER" ]]; then
    echo "Error: Asegúrate de que PROJECT_NAME, REPO_NAME y SERVER_USER estén definidos en $CONFIG_FILE."
    exit 1
fi

# Rutas
APP_DIR="/home/$SERVER_USER/$REPO_NAME"
VENV_PATH="$APP_DIR/venv/bin"
GUNICORN_SERVICE="/etc/systemd/system/gunicorn.service"

# Crear archivo de servicio para Gunicorn
echo "Creando archivo de servicio para Gunicorn en $GUNICORN_SERVICE"
sudo bash -c "cat > $GUNICORN_SERVICE" << EOL
[Unit]
Description=Gunicorn instance to serve $PROJECT_NAME
After=network.target

[Service]
User=$SERVER_USER
Group=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$VENV_PATH"
ExecStart=$VENV_PATH/gunicorn --workers 3 --bind unix:$APP_DIR/$PROJECT_NAME.sock -m 007 wsgi:application

[Install]
WantedBy=multi-user.target
EOL

# Recargar demonios de systemd para que reconozcan el nuevo servicio
echo "Recargando demonios de systemd"
sudo systemctl daemon-reload

# Iniciar y habilitar el servicio de Gunicorn
echo "Iniciando y habilitando Gunicorn"
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Comprobar el estado del servicio
echo "Verificando estado de Gunicorn"
sudo systemctl status gunicorn --no-pager
