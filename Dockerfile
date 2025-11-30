# Imagen base
FROM public.ecr.aws/docker/library/python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de la app
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install newrelic
ENV NEW_RELIC_APP_NAME="Nombre_de_su_App"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LICENSE_KEY=Su_INGEST_License
ENV NEW_RELIC_LOG_LEVEL=info

# Copiar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto Flask
EXPOSE 8000

# Comando de ejecución
CMD ["NEW_RELIC_CONFIG_FILE=newrelic.ini", "newrelic-admin", "run-program","gunicorn", "--bind", "0.0.0.0:8000", "main:app"]


# Prueba