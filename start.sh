#!/bin/bash
# Script universal para detectar el puerto serie del Arduino y lanzar el contenedor Docker
# Compatible con Linux y MacOS

# Detectar puerto Arduino
PORT=""
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  PORT=$(ls /dev/ttyACM* /dev/ttyUSB* 2>/dev/null | head -n 1)
elif [[ "$OSTYPE" == "darwin"* ]]; then
  PORT=$(ls /dev/tty.usbmodem* /dev/tty.usbserial* 2>/dev/null | head -n 1)
fi

if [ -z "$PORT" ]; then
  echo "No se detectó Arduino conectado. Conéctalo por USB y vuelve a intentar."
  exit 1
fi

echo "Puerto detectado: $PORT"

docker run -it --rm \
  --device=$PORT \
  -p 8501:8501 \
  arduino-temp-dashboard &

# Espera unos segundos y abre el navegador
sleep 5
if which xdg-open > /dev/null; then
  xdg-open http://localhost:8501
elif which open > /dev/null; then
  open http://localhost:8501
fi
