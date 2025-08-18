import os
import sys


def main():
    """Lanza la aplicación de escritorio.

    Cuando está empaquetado con PyInstaller en --onefile, es preferible
    importar y llamar a la función `main` de `dashboard_tkinter` directamente
    en lugar de ejecutar un subprocess sobre el archivo fuente (que no
    existirá en el bundle).
    """
    print("🌡️ Dashboard de Temperatura NTC - Versión Desktop")
    print("=" * 55)

    try:
        # Intentar importar el módulo local (funciona cuando se ejecuta con Python
        # y cuando PyInstaller incluye el módulo en el bundle).
        import dashboard_tkinter

        print("🚀 Iniciando dashboard de escritorio (import)...")
        # Llamar al entrypoint definido en dashboard_tkinter
        if hasattr(dashboard_tkinter, 'main'):
            dashboard_tkinter.main()
        else:
            # Fallback: ejecutar como script si no hay main()
            exec(open(os.path.join(os.path.dirname(__file__), 'dashboard_tkinter.py')).read(), {})

    except Exception as e:
        # Fallback a intentar ejecutar el archivo como proceso externo (antiguo comportamiento)
        try:
            app_path = os.path.join(os.path.dirname(__file__), 'dashboard_tkinter.py')
            if os.path.exists(app_path):
                print("🚀 Iniciando dashboard de escritorio (subprocess)...")
                import subprocess
                subprocess.run([sys.executable, app_path], check=True)
            else:
                print(f"❌ No se encontró ni el módulo ni el archivo: {app_path}")
                input("Presiona Enter para salir...")
        except FileNotFoundError:
            print("❌ Error: Python no encontrado")
            input("Presiona Enter para salir...")
        except Exception as ex:
            print(f"❌ Error: {ex}")
            input("Presiona Enter para salir...")


if __name__ == "__main__":
    main()
