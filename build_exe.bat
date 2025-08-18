@echo off
setlocal
title Build Dashboard .exe - PyInstaller helper
echo.
echo ==============================================
echo   Build: Dashboard_IoT.exe (PyInstaller)
echo ==============================================
echo.

REM Prefer virtualenv in repo
if exist "%~dp0iot_local_311\Scripts\activate.bat" (
    echo Activando entorno virtual local...
    call "%~dp0iot_local_311\Scripts\activate.bat"
)

REM Asegurar pyinstaller
echo Verificando PyInstaller...
python -c "import sys; import pkgutil; print('PYTHON', sys.executable); raise SystemExit(0)" 2>nul
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller no encontrado. Instalando...
    pip install pyinstaller>=5.11.0
)

echo Iniciando build (esto puede tardar algunos minutos)...

REM Ejecutar pyinstaller. --collect-data matplotlib ayuda a incluir datos de matplotlib.
pyinstaller --noconfirm --onefile --windowed --name Dashboard_IoT --collect-data matplotlib run_desktop.py

if errorlevel 1 (
    echo.
    echo ❌ Fallo en la generación del .exe. Revisa la salida anterior para errores.
    pause
    exit /b 1
)

REM Copiar binario a carpeta release
if not exist "%~dp0release" mkdir "%~dp0release"
copy /y "%~dp0dist\Dashboard_IoT.exe" "%~dp0release\Dashboard_IoT.exe" >nul

echo.
echo ✅ Build finalizado. Ejecutable disponible en: %~dp0release\Dashboard_IoT.exe
echo Nota: el primer lanzamiento en máquinas nuevas puede activar alertas de antivirus.
echo.
pause
