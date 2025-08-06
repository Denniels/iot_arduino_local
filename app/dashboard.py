import streamlit as st
import serial
import serial.tools.list_ports
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time

# 📌 Configuración del sensor
ADC_MAX = 1023
VCC = 5.0
R_FIXED = 10000  # Ohmios
BETA = 3950      # Constante beta del NTC
T0 = 298.15      # Temperatura de referencia en Kelvin (25°C)
R0 = 10000       # Resistencia del NTC a 25°C

# 🎯 Función para convertir ADC a temperatura
def adc_to_temp(adc_value):
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

# 🔌 Autodetección del puerto COM
def detect_serial_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "Arduino" in p.description or "USB" in p.description:
            return p.device
    return None

# 📈 Inicialización
st.set_page_config(page_title="Monitor de Temperatura NTC", layout="wide")
st.markdown("<h1 style='text-align: center; color: #007ACC;'>🌡️ Dashboard de Temperatura NTC - Arduino + Streamlit</h1>", unsafe_allow_html=True)

# 📦 Inicializar conexión Serial
port = detect_serial_port()
if not port:
    st.error("⚠️ No se detectó un puerto Arduino. Conéctalo y reinicia la app.")
    st.stop()

ser = serial.Serial(port, 9600, timeout=1)
time.sleep(2)  # Esperar a que el puerto se estabilice

# 🧪 Variables de almacenamiento
data = []

# 🔄 Loop de lectura
placeholder = st.empty()
start_time = time.time()

while True:
    try:
        line = ser.readline().decode().strip()
        if line.isdigit():
            adc = int(line)
            temp = adc_to_temp(adc)
            timestamp = time.strftime("%H:%M:%S", time.localtime())
            data.append({"Hora": timestamp, "ADC": adc, "Temperatura (°C)": temp})

            # 🧮 DataFrame
            df = pd.DataFrame(data[-100:])  # Últimos 100 datos

            with placeholder.container():
                col1, col2 = st.columns([2, 1])

                # 📊 Gráfico de área bajo la curva
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df["Hora"],
                    y=df["Temperatura (°C)"],
                    mode="lines+markers",
                    fill="tozeroy",
                    line=dict(color="orange"),
                    marker=dict(color="red", size=6),
                    name="Temperatura"
                ))
                fig.update_layout(
                    title="📈 Temperatura en Tiempo Real",
                    xaxis_title="Hora",
                    yaxis_title="Temperatura (°C)",
                    height=400,
                    margin=dict(t=40, b=20),
                    template="plotly_white"
                )
                col1.plotly_chart(fig, use_container_width=True)

                # 🥧 Gráfico de torta ADC
                adc_counts = df["ADC"].value_counts().reset_index()
                adc_counts.columns = ["ADC", "Frecuencia"]
                pie = px.pie(adc_counts, names="ADC", values="Frecuencia", title="🥧 Distribución de Valores ADC")
                col2.plotly_chart(pie, use_container_width=True)

                # 📋 Tabla comparativa
                st.markdown("### 📋 Últimos Datos")
                st.dataframe(df[::-1], use_container_width=True)

        time.sleep(1)

    except Exception as e:
        st.error(f"Error: {e}")
        break