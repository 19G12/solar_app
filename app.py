import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set Streamlit page config
st.set_page_config(page_title="IV Curve Simulator", layout="centered")

st.title("📈 Solar PV IV Curve Simulator")
st.markdown(
    "Adjust the irradiance using the slider below and observe the corresponding IV curve.")

# Irradiance input
irradiance = st.slider("Select Irradiance (W/m²)",
                       min_value=100, max_value=1000, step=100, value=1000)

# Constants
q = 1.602e-19      # Charge of electron (C)
k = 1.381e-23      # Boltzmann constant (J/K)
T = 300            # Temperature in Kelvin
n = 1.3            # Ideality factor
I0 = 1e-10         # Reverse saturation current (A)
Vt = n * k * T / q  # Thermal voltage

# Voltage and current calculations
V = np.linspace(0, 0.8, 300)
Iph_base = 5.0  # A at 1000 W/m²
Iph = Iph_base * (irradiance / 1000)
I = Iph - I0 * (np.exp(V / Vt) - 1)
I = np.clip(I, 0, None)  # Clip negative currents

# Plotting
fig, ax = plt.subplots()
ax.plot(V, I, color='blue', label=f'{irradiance} W/m²')
ax.set_title("IV Curve")
ax.set_xlabel("Voltage (V)")
ax.set_ylabel("Current (A)")
ax.grid(True)
ax.legend()
st.pyplot(fig)
