import os
import sys
import subprocess

def main():
    print("🌡️ Dashboard de Temperatura NTC - Versión Desktop")
    print("=" * 55)
    
    # Buscar el archivo dashboard_tkinter.py
    if getattr(sys, 'frozen', False):
        # Si está empaquetado como .exe
        base_path = sys._MEIPASS
    else:
        # Si se ejecuta normalmente
        base_path = os.path.dirname(__file__)
    
    app_path = os.path.join(base_path, 'dashboard_tkinter.py')
    
    if not os.path.exists(app_path):
        print(f"❌ Error: No se encontró {app_path}")
        input("Presiona Enter para salir...")
        return
    
    try:
        print("🚀 Iniciando dashboard de escritorio...")
        
        # Ejecutar directamente el archivo Python
        subprocess.run([sys.executable, app_path], check=True)
        
    except FileNotFoundError:
        print("❌ Error: Python no encontrado")
        input("Presiona Enter para salir...")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
