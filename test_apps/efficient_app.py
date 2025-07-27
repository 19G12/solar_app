# app2_optimized.py
import streamlit as st
import datetime

st.title("PV Simulator – Optimized (Manual Run)")

# Timestamp to check rerun
st.write("Last run time:", datetime.datetime.now())

# Form-based input
with st.form("pv_input_form"):
    irradiance = st.slider("Irradiance (W/m²)", 200, 1000, 600, step=50)
    temperature = st.slider("Temperature (°C)", 10, 60, 25, step=5)
    submit = st.form_submit_button("Run Simulation")

# Execute logic only when button is pressed
if submit:
    voltage = 30 - (temperature - 25) * 0.2
    current = irradiance * 0.005
    st.success("Simulation Complete!")
    st.write(f"Voltage: {voltage:.2f} V")
    st.write(f"Current: {current:.2f} A")
