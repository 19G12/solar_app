import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="IV Curve Simulator", layout="centered")

st.title("📈 Solar PV IV Curve Simulator")
st.markdown(
    "Adjust the irradiance using the slider below and observe the corresponding IV curve.")

irradiance = st.slider("Select Irradiance (W/m²)",
                       min_value=100, max_value=1000, step=100, value=1000)

st.markdown(
    "Adjust the temperature using the slider below to see changes in graph °C"
)
temperature = st.slider("Select the temperature (°C)",
                        min_value=-10, max_value=100, step=5, value=25
                        )  # Add atemperature slider

q = 1.602e-19
k = 1.381e-23
T = temperature + 273.5            # Temperature in Kelvin
n = 1.3
I0 = 1e-10         # Reverse saturation current (A)
Vt = n * k * T / q  # Thermal voltage

V = np.linspace(0, 0.8, 300)
Iph_base = 5.0  # A at 1000 W/m²
Iph = Iph_base * (irradiance / 1000)*(1 + 0.0006*(temperature - 25))
I0_t = I0 * np.exp(0.0002 * (temperature - 25))
I = Iph - I0_t * (np.exp(V / Vt) - 1)
I = np.clip(I, 0, None)

fig, ax = plt.subplots()
ax.plot(V, I, color='blue', label=f'{irradiance} W/m²')
ax.set_title("IV Curve")
ax.set_xlabel("Voltage (V)")
ax.set_ylabel("Current (A)")
ax.grid(True)
ax.legend()
st.pyplot(fig)
