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
if [[ -z "$PROJECT_NAME" || -z "$REPO_NAME" || -z "$PUBLIC_IP" ]]; then
    echo "Error: Asegúrate de que PROJECT_NAME, REPO_NAME y PUBLIC_IP estén definidos en $CONFIG_FILE."
    exit 1
fi

# Rutas
USER="ubuntu"  # Cambiar si tu usuario no es ubuntu
APP_DIR="/home/$USER/$REPO_NAME"
NGINX_SITES_AVAILABLE="/etc/nginx/sites-available/$PROJECT_NAME"
NGINX_SITES_ENABLED="/etc/nginx/sites-enabled/$PROJECT_NAME"

# Crear archivo de configuración para Nginx
echo "Creando archivo de configuración de Nginx en $NGINX_SITES_AVAILABLE"
sudo bash -c "cat > $NGINX_SITES_AVAILABLE" << EOL
server {
    listen 80;
    server_name $PUBLIC_IP;
    location / {
        include proxy_params;
        proxy_pass http://unix:$APP_DIR/$PROJECT_NAME.sock;
    }
}
EOL

# Enlazar configuración a sites-enabled
echo "Enlazando configuración de Nginx a sites-enabled"
if [ -L "$NGINX_SITES_ENABLED" ]; then
    echo "El enlace ya existe. Actualizando..."
    sudo rm "$NGINX_SITES_ENABLED"
fi
sudo ln -s $NGINX_SITES_AVAILABLE $NGINX_SITES_ENABLED

# Probar configuración de Nginx
echo "Probando configuración de Nginx"
sudo nginx -t

# Reiniciar Nginx si la prueba fue exitosa
if [ $? -eq 0 ]; then
    echo "Reiniciando Nginx"
    sudo systemctl reload nginx
else
    echo "Error en la configuración de Nginx. Revísala antes de continuar."
fi
