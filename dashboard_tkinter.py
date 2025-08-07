import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import pandas as pd
import numpy as np
import time
import threading

# 📌 Configuración del sensor
ADC_MAX = 1023
VCC = 5.0
R_FIXED = 10000  # Ohmios
BETA = 3950      # Constante beta del NTC
T0 = 298.15      # Temperatura de referencia en Kelvin (25°C)
R0 = 10000       # Resistencia del NTC a 25°C

class TemperatureDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("🌡️ Dashboard de Temperatura NTC - Arduino IoT")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Variables de datos
        self.data = []
        self.ser = None
        self.is_running = False
        
        # Crear interfaz
        self.create_widgets()
        
        # Intentar conectar Arduino automáticamente
        self.auto_connect()
    
    def adc_to_temp(self, adc_value):
        """Convierte valor ADC a temperatura"""
        if adc_value == 0:
            return None
        v_out = adc_value * VCC / ADC_MAX
        r_ntc = (v_out * R_FIXED) / (VCC - v_out)
        
        try:
            temp_k = 1 / (1 / T0 + (1 / BETA) * np.log(r_ntc / R0))
            temp_c = temp_k - 273.15
            return round(temp_c, 2)
        except:
            return None
    
    def detect_serial_port(self):
        """Detecta el puerto del Arduino"""
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "Arduino" in p.description or "USB" in p.description or "CH340" in p.description:
                return p.device
        return None
    
    def create_widgets(self):
        """Crea la interfaz gráfica"""
        # Título
        title_frame = tk.Frame(self.root, bg='#2E86AB', height=80)
        title_frame.pack(fill='x', padx=10, pady=10)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🌡️ Dashboard de Temperatura NTC - Arduino + Tkinter", 
                              font=('Arial', 18, 'bold'), fg='white', bg='#2E86AB')
        title_label.pack(expand=True)
        
        # Frame de control
        control_frame = tk.Frame(self.root, bg='#f0f0f0')
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Estado de conexión
        self.status_label = tk.Label(control_frame, text="❌ Arduino desconectado", 
                                   font=('Arial', 12), fg='red', bg='#f0f0f0')
        self.status_label.pack(side='left')
        
        # Botones
        self.connect_btn = tk.Button(control_frame, text="🔌 Conectar Arduino", 
                                   command=self.connect_arduino, bg='#28a745', fg='white',
                                   font=('Arial', 10, 'bold'))
        self.connect_btn.pack(side='right', padx=5)
        
        self.disconnect_btn = tk.Button(control_frame, text="❌ Desconectar", 
                                      command=self.disconnect_arduino, bg='#dc3545', fg='white',
                                      font=('Arial', 10, 'bold'), state='disabled')
        self.disconnect_btn.pack(side='right', padx=5)
        
        # Frame principal con gráfico y datos
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Frame del gráfico
        graph_frame = tk.Frame(main_frame, bg='white', relief='solid', bd=1)
        graph_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Configurar matplotlib
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.ax.set_title('📈 Temperatura en Tiempo Real', fontsize=14, fontweight='bold')
        self.ax.set_xlabel('Tiempo')
        self.ax.set_ylabel('Temperatura (°C)')
        self.ax.grid(True, alpha=0.3)
        
        self.canvas = FigureCanvasTkAgg(self.fig, graph_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame de datos
        data_frame = tk.Frame(main_frame, bg='white', relief='solid', bd=1, width=350)
        data_frame.pack(side='right', fill='y', padx=(5, 0))
        data_frame.pack_propagate(False)
        
        # Datos actuales
        current_frame = tk.Frame(data_frame, bg='white')
        current_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(current_frame, text="📊 Datos Actuales", font=('Arial', 14, 'bold'), 
                bg='white').pack()
        
        self.temp_var = tk.StringVar(value="-- °C")
        self.adc_var = tk.StringVar(value="-- ADC")
        self.time_var = tk.StringVar(value="--:--:--")
        
        temp_frame = tk.Frame(current_frame, bg='#e8f5e8', relief='solid', bd=1)
        temp_frame.pack(fill='x', pady=5)
        tk.Label(temp_frame, text="🌡️ Temperatura:", font=('Arial', 11, 'bold'), 
                bg='#e8f5e8').pack(side='left', padx=5, pady=5)
        tk.Label(temp_frame, textvariable=self.temp_var, font=('Arial', 11), 
                bg='#e8f5e8', fg='#d9534f').pack(side='right', padx=5, pady=5)
        
        adc_frame = tk.Frame(current_frame, bg='#e8f4fd', relief='solid', bd=1)
        adc_frame.pack(fill='x', pady=5)
        tk.Label(adc_frame, text="⚡ Valor ADC:", font=('Arial', 11, 'bold'), 
                bg='#e8f4fd').pack(side='left', padx=5, pady=5)
        tk.Label(adc_frame, textvariable=self.adc_var, font=('Arial', 11), 
                bg='#e8f4fd', fg='#337ab7').pack(side='right', padx=5, pady=5)
        
        time_frame = tk.Frame(current_frame, bg='#fff3cd', relief='solid', bd=1)
        time_frame.pack(fill='x', pady=5)
        tk.Label(time_frame, text="🕒 Última lectura:", font=('Arial', 11, 'bold'), 
                bg='#fff3cd').pack(side='left', padx=5, pady=5)
        tk.Label(time_frame, textvariable=self.time_var, font=('Arial', 11), 
                bg='#fff3cd', fg='#856404').pack(side='right', padx=5, pady=5)
        
        # Tabla de datos
        table_frame = tk.Frame(data_frame, bg='white')
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(table_frame, text="📋 Historial de Datos", font=('Arial', 12, 'bold'), 
                bg='white').pack()
        
        # Crear tabla
        columns = ('Hora', 'ADC', 'Temp (°C)')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, anchor='center')
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def auto_connect(self):
        """Intenta conectar automáticamente al Arduino"""
        port = self.detect_serial_port()
        if port:
            self.connect_to_port(port)
    
    def connect_arduino(self):
        """Conecta manualmente al Arduino"""
        port = self.detect_serial_port()
        if port:
            self.connect_to_port(port)
        else:
            messagebox.showerror("Error", "No se detectó ningún Arduino.\n\nAsegúrate de que esté conectado y que los drivers estén instalados.")
    
    def connect_to_port(self, port):
        """Conecta a un puerto específico"""
        try:
            if self.ser:
                self.ser.close()
            
            self.ser = serial.Serial(port, 9600, timeout=1)
            time.sleep(2)  # Esperar estabilización
            
            self.status_label.config(text=f"✅ Arduino conectado en {port}", fg='green')
            self.connect_btn.config(state='disabled')
            self.disconnect_btn.config(state='normal')
            
            # Iniciar lectura de datos
            self.is_running = True
            self.read_thread = threading.Thread(target=self.read_data, daemon=True)
            self.read_thread.start()
            
            # Iniciar animación del gráfico
            self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=1000, blit=False)
            
        except Exception as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar al puerto {port}:\n\n{e}")
    
    def disconnect_arduino(self):
        """Desconecta el Arduino"""
        self.is_running = False
        if self.ser:
            self.ser.close()
            self.ser = None
        
        self.status_label.config(text="❌ Arduino desconectado", fg='red')
        self.connect_btn.config(state='normal')
        self.disconnect_btn.config(state='disabled')
        
        # Parar animación
        if hasattr(self, 'ani'):
            self.ani.event_source.stop()
    
    def read_data(self):
        """Lee datos del Arduino en hilo separado"""
        while self.is_running and self.ser:
            try:
                line = self.ser.readline().decode().strip()
                if line.isdigit():
                    adc = int(line)
                    temp = self.adc_to_temp(adc)
                    timestamp = time.strftime("%H:%M:%S")
                    
                    # Agregar datos
                    self.data.append({
                        "Hora": timestamp,
                        "ADC": adc,
                        "Temperatura": temp
                    })
                    
                    # Mantener solo últimos 100 puntos
                    if len(self.data) > 100:
                        self.data = self.data[-100:]
                    
                    # Actualizar interfaz (thread-safe)
                    self.root.after(0, self.update_ui, timestamp, adc, temp)
                
            except Exception as e:
                if self.is_running:
                    self.root.after(0, lambda: messagebox.showerror("Error de lectura", f"Error leyendo datos: {e}"))
                break
    
    def update_ui(self, timestamp, adc, temp):
        """Actualiza la interfaz con nuevos datos"""
        # Actualizar etiquetas
        self.time_var.set(timestamp)
        self.adc_var.set(f"{adc}")
        self.temp_var.set(f"{temp:.1f} °C" if temp else "-- °C")
        
        # Actualizar tabla (insertar al principio)
        self.tree.insert('', 0, values=(timestamp, adc, f"{temp:.1f}" if temp else "--"))
        
        # Mantener solo 50 filas visibles
        children = self.tree.get_children()
        if len(children) > 50:
            for child in children[50:]:
                self.tree.delete(child)
    
    def update_plot(self, frame):
        """Actualiza el gráfico"""
        if len(self.data) == 0:
            return
        
        # Limpiar gráfico
        self.ax.clear()
        
        # Configurar gráfico
        self.ax.set_title('📈 Temperatura en Tiempo Real', fontsize=14, fontweight='bold')
        self.ax.set_xlabel('Tiempo')
        self.ax.set_ylabel('Temperatura (°C)')
        self.ax.grid(True, alpha=0.3)
        
        # Datos para graficar
        times = [d["Hora"] for d in self.data]
        temps = [d["Temperatura"] for d in self.data if d["Temperatura"] is not None]
        times_valid = [d["Hora"] for d in self.data if d["Temperatura"] is not None]
        
        if len(temps) > 0:
            # Crear gráfico de línea con área
            self.ax.plot(times_valid, temps, 'o-', color='orange', linewidth=2, markersize=4)
            self.ax.fill_between(times_valid, temps, alpha=0.3, color='orange')
            
            # Mostrar solo cada N etiquetas en X para evitar superposición
            if len(times) > 10:
                step = len(times) // 10
                self.ax.set_xticks(times[::step])
            
            # Rotar etiquetas del eje X
            plt.setp(self.ax.get_xticklabels(), rotation=45, ha='right')
        
        # Ajustar layout
        self.fig.tight_layout()
        
        # Redibujar
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = TemperatureDashboard(root)
    
    def on_closing():
        if app.ser:
            app.disconnect_arduino()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
