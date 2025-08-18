# 🌡️ Dashboard de Temperatura NTC - Arduino IoT

**Aplicación de escritorio para monitoreo de temperatura en tiempo real con Arduino**

---

> Recomendado para ventas: usa el ejecutable ya compilado `release\Dashboard_IoT.exe` si el equipo de desarrollo te lo entrega — así no hace falta instalar Python ni dependencias.

## 📦 **Para el Equipo de Ventas - INSTRUCCIONES SIMPLES**

### 🚀 **Configuración inicial (Solo una vez)**
1. Descargar y descomprimir toda la carpeta del proyecto
2. (Recomendado) Si existe `release\Dashboard_IoT.exe`, simplemente ejecutar ese archivo. No se necesita instalar Python.
3. Si no hay ejecutable, hacer doble clic en: **`setup_portable.bat`** para instalar una copia portable de Python en la carpeta `python`.
4. Esperar a que termine la instalación automática

### ▶️ **Usar la aplicación (Cada demo)**
1. Conectar el Arduino al PC
2. Hacer doble clic en: **`run_simple.bat`** (o ejecutar `release\Dashboard_IoT.exe` si está disponible)
3. ¡Se abre la aplicación de escritorio automáticamente!

---

## 🔧 **Qué hace cada archivo**

| Archivo | Descripción |
|---------|-------------|
| `setup_portable.bat` | Instalador automático (ejecutar solo una vez) |
| `run_simple.bat` | Lanzador de la aplicación (usar para cada demo) |
| `dashboard_tkinter.py` | Aplicación principal de escritorio |
| `arduino/ntc_reader/ntc_reader.ino` | Código para cargar en el Arduino |

---

## 📱 **Características de la Aplicación**

### ✅ **Detección automática**
- ✅ Encuentra el Arduino automáticamente
- ✅ Compatible con Arduino UNO, Nano, clones CH340
- ✅ Detección de puerto COM automática

### 📊 **Dashboard en tiempo real**
- 📈 Gráfico de temperatura con área bajo la curva
- 📋 Tabla de datos históricos
- 🌡️ Temperatura actual en tiempo real
- ⚡ Valores ADC del sensor
- 🕒 Marcas de tiempo precisas

### 🎨 **Interfaz profesional**
- 🖥️ Aplicación nativa de escritorio
- 🎯 Botones de conexión/desconexión
- 📊 Datos actuales destacados
- 📈 Gráfico interactivo
- 🗂️ Historial de 100 lecturas

---

## 🔌 **Hardware requerido**

- **Arduino UNO** (o compatible)
- **Sensor NTC 10KΩ**
- **Resistencia fija 10KΩ**
- **Protoboard y cables**

### 🔧 **Conexiones**
```
NTC Sensor:
- Un terminal → 5V (Arduino)
- Otro terminal → A0 y resistencia de 10KΩ
- Resistencia de 10KΩ → GND
```

---

## 📂 **Estructura del proyecto**

```
📁 Proyecto/
├── 🚀 setup_portable.bat       # Instalador automático
├── ▶️ run_simple.bat           # Lanzador de la app
├── 🖥️ dashboard_tkinter.py     # Aplicación principal
├── 📁 arduino/
│   └── 📁 ntc_reader/
│       └── 🔧 ntc_reader.ino   # Código Arduino
├── 📁 app/
│   └── 🌐 dashboard.py         # Versión web (Streamlit)
└── 📄 requirements.txt         # Dependencias Python
```

---

## ❓ **Solución de problemas**

### ❌ **"No se detectó Arduino"**
- ✅ Verificar que el Arduino esté conectado
- ✅ Instalar drivers CH340 si es un clon
- ✅ Verificar que el sketch esté cargado
- ✅ Cerrar IDE de Arduino u otros monitores serie

### ❌ **"Error al ejecutar aplicación"**
- ✅ Ejecutar `setup_portable.bat` nuevamente
- ✅ Verificar conexión USB
- ✅ Reiniciar el PC si es necesario

### ❌ **"Python no encontrado"**
- ✅ Ejecutar `setup_portable.bat` (instala Python automáticamente)
- ✅ Reiniciar el terminal/PC

---

## 🎯 **Para Desarrolladores**

### 🛠️ **Dependencias**
```
pyserial==3.5
matplotlib>=3.7.0
pandas>=2.0.0
numpy>=1.24.0
tkinter (incluido con Python)
```

### 🚀 **Desarrollo**
```bash
# Activar entorno virtual
iot_local_311\Scripts\activate

# Ejecutar aplicación
python dashboard_tkinter.py

# Versión web (alternativa)
streamlit run app/dashboard.py
```

---

## 📄 **Licencia**
Este proyecto es para uso interno y demostraciones comerciales.

---

## 📞 **Soporte**
Para problemas técnicos o consultas, contactar al equipo de desarrollo.

---

**¡Listo para mostrar a los clientes! 🚀**
