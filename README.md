📦 Proyecto: Monitor de Temperatura con Arduino + Streamlit + Docker
🧩 Descripción
Este proyecto permite visualizar en tiempo real la temperatura medida por un sensor NTC de 10 kΩ conectado a un Arduino. La lectura se realiza vía USB desde un PC con Windows, y se muestra en un dashboard local desarrollado con Streamlit. Todo el entorno corre dentro de un contenedor Docker, facilitando el despliegue para equipos comerciales sin conocimientos técnicos.

🛠️ Hardware Requerido
- Arduino UNO (o compatible)
- Sensor NTC 10 kΩ
- Resistencia fija 10 kΩ
- Cable USB para conexión al PC

Esquema de conexión:

```
5V --- [R 10kΩ] --- A0 --- [NTC 10kΩ] --- GND
```

📁 Estructura del Proyecto
```
arduino_iot_local/
├── arduino/
│   └── ntc_reader.ino           # Código Arduino para enviar datos por Serial
├── app/
│   └── dashboard.py             # App Streamlit que lee datos y muestra gráfico
├── requirements.txt             # Dependencias Python para Streamlit
├── Dockerfile                   # Imagen Docker con entorno Python + Streamlit
├── .dockerignore
├── README.md                    # Este archivo
└── start.sh                     # Script de arranque para Windows
```

📋 Requisitos de Software

🚀 Instrucciones de Instalación
1. ✅ Requisitos previos
📋 Requisitos de Software
- Windows 10/11, MacOS o Linux
- Docker Desktop instalado ([Descargar Docker Desktop](https://www.docker.com/products/docker-desktop/))
- Arduino UNO (o compatible) conectado por USB

> **Nota:** No necesitas instalar Python ni dependencias manualmente. Todo corre dentro de Docker.
    - Windows 10/11
    - Docker Desktop instalado
    - Arduino conectado por USB
2. 🔌 Cargar el código en el Arduino
    - Abre el IDE de Arduino.
2. 🔌 Carga el código en el Arduino
    - Abre el IDE de Arduino.
    - Carga el archivo `arduino/ntc_reader.ino`.
    - Selecciona el puerto correcto y sube el sketch.

3. 📦 Clona este repositorio
```bash
git clone https://github.com/tu-usuario/arduino-temp-dashboard.git
cd arduino-temp-dashboard
```

4. 🐳 Construye la imagen Docker (solo la primera vez o tras cambios)
```bash
docker build -t arduino-temp-dashboard .
```

5. ▶️ Ejecuta la app automáticamente

### Windows
Ejecuta el script PowerShell (haz clic derecho y elige "Ejecutar con PowerShell"):
```powershell
./start.ps1
```

### Linux/MacOS
Da permisos y ejecuta el script:
```bash
chmod +x start.sh
./start.sh
```

El script detectará el puerto del Arduino, lanzará el contenedor y abrirá el navegador en http://localhost:8501 automáticamente.
📊 Dashboard

� **Automatización total:**
No necesitas saber el puerto ni comandos de Docker. Solo ejecuta el script correspondiente y todo funcionará automáticamente.
Una vez levantado el contenedor, abre tu navegador en:
Al ejecutarse el script, se abrirá automáticamente tu navegador en:
http://localhost:8501

Verás un gráfico en tiempo real con la temperatura estimada a partir del sensor NTC.

� Código Arduino (ntc_reader.ino)

---

## 🛟 Soporte y dudas
Si tienes problemas con Docker Desktop o la detección del Arduino, revisa:
- ¿Está Docker Desktop corriendo?
- ¿El Arduino está bien conectado y el código cargado?
- ¿Tienes permisos de administrador (Windows) o de acceso a dispositivos USB (Linux/Mac)?

Para soporte técnico, contacta al equipo de desarrollo.
```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  int adc = analogRead(A0);
  Serial.println(adc);
  delay(1000);
}
```


🐍 Código Python (dashboard.py)
- Lee datos desde el puerto serial.
- Convierte ADC a resistencia.
- Aplica fórmula Steinhart-Hart para calcular temperatura.
- Muestra gráfico en Streamlit.

🧪 Fórmula de Temperatura
Usamos la ecuación de Steinhart-Hart simplificada:
R_ntc = R_fixed * (1023.0 / adc - 1)
T_kelvin = 1 / (A + B * log(R_ntc) + C * pow(log(R_ntc), 3))
T_celsius = T_kelvin - 273.15


Coeficientes A, B, C deben ajustarse según el modelo del NTC.

Desarrollado por Daniel Mardones

## ⚠️ Aviso de derechos reservados

Este repositorio está disponible públicamente únicamente para fines de demostración de la aplicación.

Todo el código fuente, documentación y activos incluidos están protegidos por derechos de autor. No se permite su uso, copia, modificación ni distribución sin autorización explícita del autor.

🔒 Este proyecto **no está licenciado** bajo ninguna licencia de software libre o de código abierto.

📩 Si deseas colaborar, acceder al código con fines educativos o comerciales, contáctame directamente.