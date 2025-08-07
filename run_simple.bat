@echo off
title Dashboard Arduino IoT - Monitor de Temperatura

echo.
echo ========================================
echo   🌡️ Dashboard Arduino IoT
echo ========================================
echo.

REM Detectar y usar el mejor Python disponible
if exist "%~dp0python\python.exe" (
    set PYTHON_EXE=%~dp0python\python.exe
    echo 🐍 Usando Python portable
) else if exist "%~dp0iot_local_311\Scripts\python.exe" (
    set PYTHON_EXE=%~dp0iot_local_311\Scripts\python.exe
    echo 🐍 Usando entorno virtual local
) else (
    set PYTHON_EXE=python
    echo 🐍 Usando Python del sistema
)

echo 🚀 Iniciando dashboard...
echo 📱 Se abrirá una ventana con la aplicación
echo.

"%PYTHON_EXE%" "%~dp0dashboard_tkinter.py"

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error al ejecutar la aplicación
    echo 💡 Verifica que el Arduino esté conectado
    echo 💡 O ejecuta setup_portable.bat para configurar
    pause
)
