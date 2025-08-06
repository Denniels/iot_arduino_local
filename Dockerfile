# Dockerfile para Arduino Temp Dashboard
FROM python:3.11-slim

# Instala dependencias del sistema para pyserial y Streamlit
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Crea el directorio de la app
WORKDIR /app

# Copia los archivos de la app y dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/

# Expone el puerto de Streamlit
EXPOSE 8501

# Comando de arranque
CMD ["streamlit", "run", "app/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
