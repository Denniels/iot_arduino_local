import os
import sys
import subprocess
import time
import webbrowser
import socket

# Lanzador simple y robusto para el dashboard de temperatura NTC

def check_port(port):
    """Verifica si el puerto está disponible"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result == 0
    except:
        return False

def main():
    print("🌡️ Dashboard de Temperatura NTC - Arduino IoT")
    print("=" * 50)
    
    # Verificar si ya hay algo corriendo en el puerto
    if check_port(8501):
        print("⚠️ Ya hay una aplicación corriendo en el puerto 8501")
        print("📌 Abriendo navegador...")
        webbrowser.open('http://localhost:8501')
        input("\nPresiona Enter para salir...")
        return
    
    # Buscar el archivo dashboard.py
    possible_paths = [
        os.path.join(os.path.dirname(__file__), 'app', 'dashboard.py'),
        os.path.join(os.path.dirname(sys.executable), 'app', 'dashboard.py') if getattr(sys, 'frozen', False) else None,
        os.path.join(getattr(sys, '_MEIPASS', ''), 'app', 'dashboard.py') if getattr(sys, 'frozen', False) else None,
    ]
    
    app_path = None
    for path in possible_paths:
        if path and os.path.exists(path):
            app_path = path
            break
    
    if not app_path:
        print("❌ Error: No se encontró el archivo dashboard.py")
        print("📁 Buscando en:")
        for path in possible_paths:
            if path:
                print(f"   - {path}")
        input("\nPresiona Enter para salir...")
        return
    
    print(f"📁 Usando: {app_path}")
    print("⏳ Iniciando servidor...")
    
    try:
        # Intentar ejecutar directamente dashboard.py como un script de streamlit
        cmd = [sys.executable, '-m', 'streamlit', 'run', app_path, '--server.headless=true']
        
        print("🚀 Comando:", ' '.join(cmd))
        
        # Ejecutar con salida visible para debug
        proc = subprocess.Popen(cmd, 
                               cwd=os.path.dirname(app_path),
                               creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0)
        
        print("⏳ Esperando que el servidor esté listo...")
        
        # Esperar a que el servidor esté listo
        for i in range(30):
            if check_port(8501):
                print("✅ Servidor listo!")
                time.sleep(2)
                print("🌐 Abriendo navegador...")
                webbrowser.open('http://localhost:8501')
                break
            time.sleep(1)
            print(f"⏳ Esperando... ({i+1}/30)")
        else:
            print("⚠️ Timeout. Ve manualmente a: http://localhost:8501")
        
        print("\n📌 INSTRUCCIONES:")
        print("   - El dashboard está corriendo en tu navegador")
        print("   - Mantén esta ventana abierta")
        print("   - Para cerrar, presiona Ctrl+C aquí")
        print("\n🔗 URL: http://localhost:8501")
        
        try:
            proc.wait()
        except KeyboardInterrupt:
            print("\n🛑 Cerrando aplicación...")
            proc.terminate()
            
    except FileNotFoundError:
        print("❌ Error: No se encontró Python o Streamlit")
        print("💡 Solución: Instala Python y ejecuta 'pip install streamlit'")
        input("\nPresiona Enter para salir...")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        print(f"🔧 Tipo de error: {type(e).__name__}")
        input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()
