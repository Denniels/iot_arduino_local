# start.ps1 - Script PowerShell para Windows
# Detecta el puerto COM del Arduino y lanza el contenedor Docker

# Buscar todos los puertos COM disponibles
$ports = Get-WmiObject Win32_SerialPort | Select-Object DeviceID, Description


# Mostrar todos los puertos encontrados (si hay)
if ($ports) {
    Write-Host "Puertos COM detectados:"
    $ports | ForEach-Object { Write-Host ("- " + $_.DeviceID + " (" + $_.Description + ")") }
    # Intentar encontrar un puerto que contenga 'Arduino' o 'USB Serial' en la descripción
    $arduinoPort = $ports | Where-Object { $_.Description -match 'Arduino|USB Serial' } | Select-Object -First 1
    if ($arduinoPort) {
        $port = $arduinoPort.DeviceID
        Write-Host "Puerto Arduino detectado: $port"
    } else {
        $port = Read-Host "No se detectó Arduino automáticamente. Ingresa el nombre del puerto COM (ejemplo: COM5)"
    }
} else {
    Write-Host "No se detectó ningún puerto COM automáticamente."
    $port = Read-Host "Ingresa el nombre del puerto COM donde está conectado el Arduino (ejemplo: COM5)"
}

if (-not $port) {
    Write-Host "No se seleccionó ningún puerto. Abortando."
    exit 1
}

# Convertir COMx a formato Docker
$comNumber = ($port -replace 'COM', '')
$dockerPort = "/dev/ttyS$comNumber"

# Lanzar el contenedor
Start-Process -NoNewWindow -FilePath "docker" -ArgumentList @(
    "run", "-it", "--rm",
    "--privileged",
    "--device=$dockerPort",
    "-p", "8501:8501",
    "arduino-local-iot"
)

# Esperar y abrir navegador
Start-Sleep -Seconds 5
Start-Process "http://localhost:8501"
