@echo off
title Dashboard de Temperatura NTC - Arduino IoT
echo.
echo =================================================
echo   Dashboard de Temperatura NTC - Arduino IoT
echo =================================================
echo.
echo ⏳ Iniciando aplicacion...
echo.

REM Activar entorno virtual si existe
if exist "iot_local_311\Scripts\activate.bat" (
    echo 🐍 Activando entorno Python...
    call iot_local_311\Scripts\activate.bat
)

REM Verificar si Python está disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado o no está en el PATH
    echo 💡 Instala Python desde https://python.org
    pause
    exit /b 1
)

REM Verificar si Streamlit está instalado
python -m streamlit --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Streamlit no encontrado. Instalando dependencias...
    pip install -r requirements.txt
)

echo ✅ Lanzando dashboard...
echo 🌐 Se abrirá automáticamente en tu navegador
echo 📌 Para cerrar la aplicación, presiona Ctrl+C
echo.

REM Lanzar la aplicación
python -m streamlit run app\dashboard.py

echo.
echo 🛑 Dashboard cerrado.
pause
