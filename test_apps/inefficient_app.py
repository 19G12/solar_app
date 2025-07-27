import streamlit as st
import datetime

st.title("PV Simulator – Standard (Auto-Rerun)")
st.write("Last run time:", datetime.datetime.now())

irradiance = st.slider("Irradiance (W/m²)", 200, 1000, 600, step=50)
temperature = st.slider("Temperature (°C)", 10, 60, 25, step=5)

# Simple PV logic
voltage = 30 - (temperature - 25) * 0.2
current = irradiance * 0.005

st.write(f"Voltage: {voltage:.2f} V")
st.write(f"Current: {current:.2f} A")
