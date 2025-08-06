# start.ps1 - Script PowerShell para Windows
# Detecta el puerto COM del Arduino y lanza el contenedor Docker

# Buscar el primer puerto COM disponible (ajusta el filtro si tienes más de un Arduino)
$port = Get-WmiObject Win32_SerialPort | Where-Object { $_.DeviceID -like 'COM*' } | Select-Object -First 1 -ExpandProperty DeviceID

if (-not $port) {
    Write-Host "No se detectó Arduino conectado. Conéctalo por USB y vuelve a intentar."
    exit 1
}

Write-Host "Puerto detectado: $port"

# Convertir COMx a formato Docker
$dockerPort = "/dev/ttyS" + ($port -replace 'COM', '')

# Lanzar el contenedor
Start-Process -NoNewWindow -FilePath "docker" -ArgumentList @(
    "run", "-it", "--rm",
    "--device=$dockerPort",
    "-p", "8501:8501",
    "arduino-temp-dashboard"
)

# Esperar y abrir navegador
Start-Sleep -Seconds 5
Start-Process "http://localhost:8501"
