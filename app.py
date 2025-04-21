import streamlit as st
import fastf1
from fastf1 import plotting
import plotly.graph_objects as go
import pandas as pd

# Configuración inicial
st.set_page_config(page_title="F1 - Análisis de telemetría - Gustavo Vazquez - UCU", layout="wide")
fastf1.Cache.enable_cache("./cache")  # crea una carpeta cache para no recargar si se ha bajado

st.markdown("""
    <style>
        body { background-color: #0E1117; color: white; }
        .sidebar .sidebar-content { background-color: #1F2023; }
        .stSelectbox > div { color: black !important; }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Comparación de Telemetría")

year = st.sidebar.selectbox("Año", [2025,2024,2023, 2022, 2021],index=2)
event_schedule = fastf1.get_event_schedule(year)
event_names = event_schedule.loc[event_schedule['EventFormat'] != 'Testing', 'EventName'].tolist()

gp_name = st.sidebar.selectbox("Grand Prix", event_names)
session_type = st.sidebar.selectbox("Sesión", ['FP1', 'FP2', 'FP3', 'Q', 'R'])

# Cargar sesión
session = fastf1.get_session(year, gp_name, session_type)
with st.spinner('Cargando datos de sesión...'):
    session.load()

# Selección de pilotos
drivers = sorted(session.laps['Driver'].unique())
driver1 = st.sidebar.selectbox("Driver 1", drivers)
driver2 = st.sidebar.selectbox("Driver 2", [d for d in drivers if d != driver1])

# Obtener vueltas rápidas
lap1 = session.laps.pick_driver(driver1).pick_fastest()
lap2 = session.laps.pick_driver(driver2).pick_fastest()
tel1 = lap1.get_car_data().add_distance()
tel2 = lap2.get_car_data().add_distance()

# Mostrar resumen
st.subheader(f"Comparación: {driver1} vs {driver2}")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**{driver1} Tiempo:** {lap1['LapTime']}")
with col2:
    st.markdown(f"**{driver2} Tiempo:** {lap2['LapTime']}")

# Gráfico de velocidad vs. distancia
fig = go.Figure()
fig.add_trace(go.Scatter(x=tel1['Distance'], y=tel1['Speed'],
                         mode='lines', name=f'{driver1} Speed'))
fig.add_trace(go.Scatter(x=tel2['Distance'], y=tel2['Speed'],
                         mode='lines', name=f'{driver2} Speed'))

fig.update_layout(
    title=f"Comparación de velocidad - {driver1} vs {driver2}",
    xaxis_title='Distancia (m)',
    yaxis_title='Velocidad (km/h)',
    template='plotly_dark',
    height=500
)

st.plotly_chart(fig, use_container_width=True)
