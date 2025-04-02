# Usamos una imagen de python (slim porque es más ligera)
FROM python:3.9-slim

# Establecemos un directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los archivos necesarios al contenedor 
COPY . .

# Instalamos las dependencias necesarias
# usando el archivo requirements.txt
# que contiene las librerías de Flask y otras dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponemos el puerto 5000 para Flask
EXPOSE 5000

# Ejecutamos la aplicación Flask
CMD ["python", "app.py"]
