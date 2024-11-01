# Utiliza una imagen base de Python (ajusta la versión según tus necesidades)
FROM python:3.12.7-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt y instala las dependencias
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia el resto de los archivos de tu aplicación
COPY . .

# Expone el puerto en el que se ejecutará tu aplicación Flask
EXPOSE 80

# Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]