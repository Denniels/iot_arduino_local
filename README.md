# 🌡️ Dashboard de Temperatura NTC — Distribución para ventas

Este repositorio contiene la aplicación de escritorio para demostraciones comerciales. La opción recomendada para el equipo de ventas es usar el ejecutable standalone provisto en `release\Dashboard_IoT.exe`.

---

## Resumen rápido

- Ejecutable recomendado: `release\Dashboard_IoT.exe` (no requiere instalar Python ni dependencias en el PC de destino).
- Alternativa: `setup_portable.bat` + `run_simple.bat` para crear/usar un Python portable si no hay EXE.

---

## 📥 Entrega / descarga para el equipo de ventas

1. Entregar a ventas el archivo `release\Dashboard_IoT.exe` (comprimido en ZIP y compartir por email o Drive).
2. El usuario final solo necesita copiar el EXE en su PC y ejecutarlo con doble clic.

### Descargar paquete listo para ventas

Puedes descargar el paquete preparado (EXE + instrucciones) directamente desde el repositorio:

[Descargar package_for_sales.zip](release/package_for_sales.zip)

---

## 🔌 Drivers USB‑Serial (CH340) — Instalación detallada (Windows)

Por qué: muchos clones de Arduino usan el chip CH340/CH341 para la interfaz USB‑serie. En Windows es necesario instalar un driver para que el sistema operativo reconozca el dispositivo y le asigne un puerto COM. Sin este driver la aplicación no podrá abrir el puerto serie y no verá datos del Arduino.

> Enlace de descarga recomendado del driver CH340:
>
> https://sparks.gogo.co.nz/ch340.html?srsltid=AfmBOoq_0ddfkwxe6LtH_hxFROzhCRRxH6uvp7n-TejZI9Ye2NB-9_GY

### Pasos detallados de instalación en Windows

1. Desde el PC de la demo, abre el navegador y navega al enlace anterior.
2. Busca la sección "CH340 driver" o similar y descarga la versión para Windows (archivo .zip o instalador `.exe`). Normalmente se llama algo como `CH341SER.zip` o `SETUP.EXE`.
3. Si descargaste un ZIP, extrae su contenido a una carpeta.
4. Ejecuta el instalador (`setup.exe`) con permisos de administrador: clic derecho → "Ejecutar como administrador".
5. Sigue el asistente de instalación hasta completar.
6. Conecta el Arduino por USB.
7. Abre el "Administrador de dispositivos" (Win+R → `devmgmt.msc`) y verifica que aparece `USB‑SERIAL CH340 (COMx)` bajo *Puertos (COM & LPT)*.
8. Ejecuta `release\Dashboard_IoT.exe`.

### Verificación rápida

- En Device Manager debe aparecer `USB‑SERIAL CH340 (COMx)`.
- La aplicación debe mostrar "Arduino conectado en COMx".

### Solución de problemas comunes

- Si no aparece: prueba otro cable USB o puerto USB del PC.
- Si aparece con un triángulo amarillo: reinstala el driver con permisos administrativos.
- Si el COM está en uso: cierra otros programas que puedan usarlo (IDE de Arduino, PuTTY, etc.).
- Si Windows bloquea el instalador: permite la ejecución temporalmente o consulta a IT.

---

## ▶️ Cómo ejecutar

- Opción recomendada (más simple): copiar `release\Dashboard_IoT.exe` al PC y ejecutar con doble clic.

- Opción alternativa (si no hay EXE): ejecutar `setup_portable.bat` (crea una carpeta `python` con Python embeddable) y luego `run_simple.bat`.

---

## Archivos importantes

- `release\Dashboard_IoT.exe` — Ejecutable standalone (entregar a ventas).
- `run_simple.bat` — Lanzador que usa el EXE si existe o ejecuta el script con el Python portable.
- `setup_portable.bat` — Crea un Python embeddable e instala dependencias (si no se usa el EXE).
- `dashboard_tkinter.py` — Código fuente de la aplicación de escritorio (para desarrollo).

---

## Licencia y contacto

Este proyecto NO cuenta con una licencia de código abierto. Se publica en este repositorio únicamente para compartirlo con un equipo específico de trabajo. Si un tercero externo desea acceder al código o colaborar, por favor solicítalo formalmente o contactame directamente.

Contactos:

- LinkedIn: [Daniel Andrés Mardones Sanhueza](https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777)

	[![](https://cdn.worldvectorlogo.com/logos/linkedin-icon-2.svg)](https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777)

- GitHub: [Denniels](https://github.com/Denniels)

	[![](https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png)](https://github.com/Denniels)
