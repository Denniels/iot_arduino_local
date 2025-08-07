@echo off
setlocal enabledelayedexpansion

title Dashboard Arduino IoT - Instalador Automatico
echo.
echo =======================================================
echo     Dashboard de Temperatura NTC - Arduino IoT
echo                 Instalador Automatico
echo =======================================================
echo.

REM Crear directorio temporal
set TEMP_DIR=%TEMP%\arduino_dashboard
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

echo [1/4] Verificando Python...

REM Verificar si Python esta instalado
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo     ✅ Python encontrado
    goto :install_deps
)

echo     ❌ Python no encontrado
echo [2/4] Descargando Python portable...

REM Descargar Python Embeddable
set PYTHON_URL=https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip
set PYTHON_ZIP=%TEMP_DIR%\python.zip

powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_ZIP%'}"

if not exist "%PYTHON_ZIP%" (
    echo     ❌ Error descargando Python
    pause
    exit /b 1
)

echo     ✅ Python descargado

REM Extraer Python
echo [3/4] Instalando Python portable...
powershell -Command "Expand-Archive -Path '%PYTHON_ZIP%' -DestinationPath '%CD%\python' -Force"

REM Configurar pip para Python embeddable
set PYTHON_DIR=%CD%\python
echo import sys; sys.path.append('Scripts') > "%PYTHON_DIR%\pip_install.py"

REM Descargar get-pip.py
powershell -Command "Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile '%PYTHON_DIR%\get-pip.py'"

REM Instalar pip
"%PYTHON_DIR%\python.exe" "%PYTHON_DIR%\get-pip.py"

:install_deps
echo [4/4] Instalando dependencias...

REM Usar Python local si existe, sino el del sistema
if exist "%CD%\python\python.exe" (
    set PYTHON_EXE=%CD%\python\python.exe
    set PIP_EXE=%CD%\python\Scripts\pip.exe
) else (
    set PYTHON_EXE=python
    set PIP_EXE=pip
)

"%PIP_EXE%" install pyserial matplotlib pandas numpy tkinter

echo.
echo ✅ ¡Instalacion completada!
echo.
echo Para ejecutar el dashboard:
echo    1. Conecta tu Arduino
echo    2. Ejecuta: run_simple.bat
echo.
pause
